"""
guardrails/input_guardrails.py
Validate incoming requests before the loop runs.

Checks:
  - Empty messages → reject immediately (no LLM call)
  - Too-long messages → reject immediately
  - Invalid images → reject immediately
  - Off-topic messages → one cheap LLM yes/no check
  - Short follow-ups → always allow (conversational continuity)

Every rejection returns a pre-built message from validators.py
so we don't waste tokens generating a response for bad input.
"""

import os
import logging

from openai import OpenAI
from app.config import OPENAI_API_KEY, OPENAI_MODEL
from app.guardrails.policy import MAX_MESSAGE_LENGTH
from app.guardrails.validators import (
    is_within_length,
    contains_blocked_content,
    is_valid_image,
    REJECTION_MESSAGES,
)

logger = logging.getLogger(__name__)

_client = OpenAI(api_key=OPENAI_API_KEY)


class InputGuardrails:
    """Validate incoming requests before the engine runs."""

    async def validate(self, message: str, image_base64: str | None = None) -> dict:
        """
        Run all input checks.

        Returns:
            {
                "allowed": bool,
                "reason": str,
                "redirect_message": str | None  (pre-built, no LLM needed)
            }
        """

        # ── Empty message ─────────────────────────────────────────────
        if not message or not message.strip():
            if not image_base64:
                return {
                    "allowed": False,
                    "reason": "empty_message",
                    "redirect_message": REJECTION_MESSAGES["empty_message"],
                }
            # Image with no text is fine — they're sending a photo to check
            return {"allowed": True, "reason": "image_only"}

        # ── Too long ──────────────────────────────────────────────────
        if not is_within_length(message, MAX_MESSAGE_LENGTH):
            return {
                "allowed": False,
                "reason": "too_long",
                "redirect_message": REJECTION_MESSAGES["too_long"],
            }

        # ── Blocked content ───────────────────────────────────────────
        if contains_blocked_content(message):
            return {
                "allowed": False,
                "reason": "blocked_content",
                "redirect_message": REJECTION_MESSAGES["off_topic"],
            }

        # ── Invalid image ─────────────────────────────────────────────
        if image_base64:
            image_check = is_valid_image(image_base64)
            if not image_check["valid"]:
                reason = image_check["reason"]
                msg_key = "image_too_small" if reason == "image_too_small" else "invalid_image"
                return {
                    "allowed": False,
                    "reason": reason,
                    "redirect_message": REJECTION_MESSAGES[msg_key],
                }
            # Valid image → always allow regardless of text
            return {"allowed": True, "reason": "has_valid_image"}

        # ── Short messages always pass (follow-ups) ───────────────────
        if len(message.strip().split()) <= 5:
            return {"allowed": True, "reason": "short_message"}

        # ── Conversational follow-ups always pass ─────────────────────
        # These are clearly continuing an existing conversation
        follow_up_phrases = [
            "explain", "confused", "don't understand", "don't get",
            "why", "how does", "what do you mean", "more simply",
            "can you", "show me", "try again", "another example",
            "go back", "repeat", "say that again", "elaborate",
            "i think", "is that right", "did i", "check my",
            "next step", "what's next", "keep going", "continue",
            "still stuck", "help me", "i'm lost", "not sure",
            "thanks", "got it", "makes sense", "i see",
        ]
        msg_lower = message.lower()
        if any(phrase in msg_lower for phrase in follow_up_phrases):
            return {"allowed": True, "reason": "follow_up"}

        # ── Topic check via LLM (longer messages only) ────────────────
        try:
            response = _client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a classifier. Determine if the user's message "
                            "is related to math, science, homework, academic help, "
                            "OR is a follow-up question in a tutoring conversation "
                            "(like asking for clarification or a simpler explanation). "
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
                    "redirect_message": REJECTION_MESSAGES["off_topic"],
                }

        except Exception as e:
            # If guardrail check fails, let the message through
            logger.warning(f"Input guardrail LLM check failed: {e}")
            return {"allowed": True, "reason": "guardrail_error_passthrough"}
