"""
guardrails.py
Safety checks and validation for the ReAct loop.

Five guardrails:
  1. Topic guardrail     — reject off-topic input before the loop runs
  2. Conversation trim   — prevent token overflow by summarizing old messages
  3. Sub-call limiter    — cap LLM sub-calls per request to control cost
  4. Response validation  — check mode compliance, length, and empty responses
  5. Tool error handling  — prevent retries on failed tools, inject fallback instructions
"""

import os
import json
import logging
from typing import Any

from openai import OpenAI

logger = logging.getLogger(__name__)

_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
_model = os.getenv("OPENAI_MODEL", "gpt-4o")

# ── Limits ────────────────────────────────────────────────────────────────
MAX_SUB_CALLS = 3           # Max LLM sub-calls (classify, analyze, solve) per request
MAX_MESSAGE_TOKENS = 40000  # Approximate token limit before truncation triggers
MAX_RESPONSE_WORDS = 200    # Soft limit on response length


# ===========================================================================
# 1. Topic Guardrail
# ===========================================================================

async def check_topic_guardrail(message: str, has_image: bool = False) -> dict:
    """
    Check if a message is math-related before running the full loop.

    Uses a cheap LLM call to determine relevance. The model decides —
    no keyword lists, no pattern matching.

    Images are always allowed (likely photos of math work).
    Empty messages are always blocked.

    Returns:
        {
            "allowed": True/False,
            "reason": str,
            "redirect_message": str or None
        }
    """
    # Images are always allowed
    if has_image:
        return {"allowed": True, "reason": "has_image"}

    # Empty messages are always blocked
    if not message or not message.strip():
        return {
            "allowed": False,
            "reason": "empty_message",
            "redirect_message": "It looks like you sent an empty message. What math problem can I help you with?",
        }

    # Short messages (5 words or less) are likely follow-ups — allow them
    if len(message.strip().split()) <= 5:
        return {"allowed": True, "reason": "short_message"}

    # Ask the model: is this math-related?
    try:
        response = _client.chat.completions.create(
            model=_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a classifier. The user sends a message intended for a math tutoring app. "
                        "Determine if the message is related to math, science, homework, or academic help. "
                        "Respond with ONLY 'yes' or 'no'. Nothing else."
                    ),
                },
                {"role": "user", "content": message},
            ],
            temperature=0,
            max_tokens=3,
        )

        answer = response.choices[0].message.content.strip().lower()

        if answer == "yes":
            return {"allowed": True, "reason": "llm_approved"}
        else:
            return {
                "allowed": False,
                "reason": "off_topic",
                "redirect_message": (
                    "I'm your math tutor — I'm best at helping with math problems, "
                    "equations, and concepts! What are you working on?"
                ),
            }

    except Exception as e:
        # If the guardrail call fails, let the message through
        logger.warning(f"Topic guardrail LLM call failed: {e}")
        return {"allowed": True, "reason": "guardrail_error_passthrough"}


# ===========================================================================
# 2. Conversation Truncation
# ===========================================================================

def truncate_conversation(messages: list[dict[str, Any]], max_tokens: int = MAX_MESSAGE_TOKENS) -> list[dict[str, Any]]:
    """
    If the messages list is getting too long, summarize older messages
    to prevent token overflow.

    Keeps:
      - messages[0]: system prompt (always)
      - messages[1]: session context (always)
      - Last 6 messages: recent conversation (always)

    Compresses: everything in between into a single summary message.

    Returns:
        The (possibly trimmed) messages list.
    """
    # Rough token estimate: 1 token ≈ 4 characters
    total_chars = sum(
        len(str(m.get("content", ""))) for m in messages
    )
    estimated_tokens = total_chars // 4

    if estimated_tokens < max_tokens:
        return messages

    if len(messages) <= 8:
        return messages

    logger.info(f"Conversation truncation: ~{estimated_tokens} tokens, {len(messages)} messages → trimming")

    # Keep system prompt + session context (first 2)
    preserved_start = messages[:2]

    # Keep last 6 messages (recent conversation)
    preserved_end = messages[-6:]

    # Everything in between gets summarized
    middle = messages[2:-6]
    if not middle:
        return messages

    summary_parts = []
    for m in middle:
        role = m.get("role", "unknown")
        content = str(m.get("content", ""))
        if len(content) > 100:
            content = content[:100] + "..."
        if role in ("user", "assistant"):
            summary_parts.append(f"{role}: {content}")

    summary_text = (
        "[Earlier conversation summarized: "
        + " | ".join(summary_parts)
        + "]"
    )

    return preserved_start + [{"role": "user", "content": summary_text}] + preserved_end


# ===========================================================================
# 3. Sub-Call Limiter
# ===========================================================================

# Tools that make their own LLM calls — currently none after removing fake tools.
# compute_math (SymPy) will be added here if it ever needs an LLM sub-call.
LLM_POWERED_TOOLS: set[str] = set()


class SubCallTracker:
    """Tracks LLM sub-calls made by tools during a single request."""

    def __init__(self, max_calls: int = MAX_SUB_CALLS) -> None:
        self._count = 0
        self._max = max_calls

    def can_call(self, tool_name: str) -> bool:
        """Check if this tool is allowed to make a sub-LLM call."""
        if tool_name not in LLM_POWERED_TOOLS:
            return True
        return self._count < self._max

    def record_call(self, tool_name: str) -> None:
        """Record that a tool made a sub-LLM call."""
        if tool_name in LLM_POWERED_TOOLS:
            self._count += 1

    @property
    def count(self) -> int:
        return self._count

    @property
    def limit_reached(self) -> bool:
        return self._count >= self._max


# ===========================================================================
# 4. Response Validation
# ===========================================================================

def validate_response(response_text: str, mode: str | None) -> dict:
    """
    Validate the agent's response against mode rules and format guidelines.

    Returns:
        {
            "valid": bool,
            "flags": list[str],
            "corrected_text": str,
        }
    """
    flags = []
    corrected = response_text

    # Empty check (critical — replace with fallback)
    if not response_text or not response_text.strip():
        flags.append("empty_response")
        corrected = "I'm not sure I understood that — could you rephrase your question or show me what you're working on?"
        return {"valid": False, "flags": flags, "corrected_text": corrected}

    # Length check (soft — flag but don't modify)
    word_count = len(response_text.split())
    if word_count > MAX_RESPONSE_WORDS:
        flags.append(f"over_length:{word_count}_words")

    # Mode compliance (soft — flag but don't modify)
    if mode == "socratic":
        stripped = response_text.rstrip()
        if not stripped.endswith("?"):
            flags.append("socratic_no_question")

    if mode == "direct":
        lower = response_text.lower()
        has_check = any(phrase in lower for phrase in [
            "make sense", "does that", "any questions", "try this",
            "key takeaway", "to summarize", "in summary",
        ])
        if not has_check:
            flags.append("direct_no_check")

    if flags:
        logger.info(f"Response validation flags: {flags}")

    return {
        "valid": len(flags) == 0,
        "flags": flags,
        "corrected_text": corrected,
    }


# ===========================================================================
# 5. Tool Error Handling
# ===========================================================================

class FailedToolTracker:
    """Tracks tools that have failed during this request to prevent retries."""

    def __init__(self) -> None:
        self._failed: set[str] = set()

    def mark_failed(self, tool_name: str) -> None:
        """Mark a tool as failed for this request."""
        self._failed.add(tool_name)

    def has_failed(self, tool_name: str) -> bool:
        """Check if this tool already failed this request."""
        return tool_name in self._failed

    def get_block_message(self, tool_name: str) -> str:
        """Get the message to return instead of calling a failed tool."""
        return json.dumps({
            "error": f"Tool '{tool_name}' already failed this request. Do not retry.",
            "instruction": "Respond to the student using the information you already have.",
        })


def wrap_tool_error(tool_name: str, error_result: str) -> str:
    """
    When a tool returns an error, wrap it with an instruction telling
    the agent not to retry and to respond with what it knows.
    """
    try:
        parsed = json.loads(error_result)
        parsed["_agent_instruction"] = (
            f"Tool '{tool_name}' failed. Do NOT call this tool again. "
            "Use the information you already have to respond to the student."
        )
        return json.dumps(parsed)
    except json.JSONDecodeError:
        return json.dumps({
            "error": error_result,
            "_agent_instruction": (
                f"Tool '{tool_name}' failed. Do NOT call this tool again. "
                "Use the information you already have to respond to the student."
            ),
        })
