"""
react_loop.py
The ReAct loop — the agent's single brain.

Combines:
  - Three-layer memory (long-term, session, short-term)
  - Mode system (socratic, direct, concept_first via prompt text)
  - Real tools from tools.py (7 tools)
  - Graph collection for the response
  - Tool call logging for transparency
  - Image support for student work photos
  - Structured assessment extraction from tool results
  - Guardrails: topic filter, token truncation, sub-call limits,
    response validation, tool error handling

Flow:
  1. Topic guardrail — reject off-topic before anything runs
  2. Load long-term memory → build system prompt
  3. Load session memory → seed short-term memory
  4. Truncate conversation if too long
  5. Loop: send messages + tools to LLM → execute tools (with limits) → feed results back
  6. Validate response
  7. Return final response + graphs + tool log + mode info + assessment data
"""

import os
import json
import logging
from typing import Any

from openai import OpenAI
from sqlalchemy.orm import Session as DBSession

from agent.prompt import build_system_prompt
from agent.memory.long_term import get_student_context
from agent.memory.session import get_session_context
from agent.memory.short_term import ShortTermMemory
from agent.tools import TOOL_SCHEMAS, execute_tool
from agent.guardrails import (
    check_topic_guardrail,
    truncate_conversation,
    SubCallTracker,
    FailedToolTracker,
    validate_response,
    wrap_tool_error,
)

logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

MAX_ITERATIONS = 8


def _extract_assessment(tool_results: dict) -> dict:
    """
    Extract structured assessment data from tool results.

    Currently only get_hint_strategy provides topic/mastery data.
    Full assessment (correctness, error types) will come from compute_math
    (SymPy) once built. For now, those fields return None and the agent's
    text response is the primary output.
    """
    assessment = {
        "topic_type": None,
        "chapter": None,
        "difficulty": None,
        "is_correct": None,
        "result": None,
        "error_types": [],
        "understanding_level": None,
        "key_concept_missed": None,
        "hints_used": 0,
    }

    # get_hint_strategy provides topic and mastery context
    hint_data = tool_results.get("get_hint_strategy")
    if hint_data:
        assessment["topic_type"] = hint_data.get("topic") if "topic" not in hint_data.get("reason", "") else None

    return assessment


async def run_agent(
    student_id: str,
    session_id: str,
    message: str,
    db: DBSession,
    selected_mode: str | None = None,
    image_base64: str | None = None,
    conversation_history: list[dict] | None = None,
) -> dict:
    """
    Run the ReAct loop for a single student message.

    Returns:
        {
            "message": str,
            "iterations": int,
            "tools_used": list[str],
            "tool_calls_made": list[dict],
            "graphs": list[dict],
            "mode_used": str,
            "mode_source": str,
            "assessment": dict,
            "is_problem": bool,
            "validation_flags": list[str],
        }
    """

    # ── Guardrail 1: Topic check ─────────────────────────────────────────
    topic_check = await check_topic_guardrail(message, has_image=bool(image_base64))
    if not topic_check["allowed"]:
        logger.info(f"Topic guardrail blocked: {topic_check['reason']}")
        return _build_return(
            topic_check["redirect_message"],
            iterations=0,
            tools_used=[],
            tool_calls_log=[],
            graphs=[],
            selected_mode=selected_mode,
            tool_results_data={},
            validation_flags=["topic_guardrail_blocked"],
        )

    # ── 1. Long-term memory → system prompt ───────────────────────────────
    student_context = await get_student_context(student_id, db)
    system_prompt = build_system_prompt(student_context)

    # ── 2. Session memory → session context string ────────────────────────
    session_context = await get_session_context(session_id, db, selected_mode)

    # ── 3. Initialize short-term memory ───────────────────────────────────
    memory = ShortTermMemory()
    memory.init(system_prompt, session_context, message, conversation_history)

    # If the student sent an image, convert the last user message to multimodal
    if image_base64:
        msgs = memory.get_messages()
        last_msg = msgs[-1]
        text_content = last_msg["content"]
        last_msg["content"] = [
            {"type": "text", "text": text_content},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{image_base64}"},
            },
        ]

    # ── Guardrail 2: Truncate conversation if too long ────────────────────
    memory._messages = truncate_conversation(memory.get_messages())

    # ── Context passed to tool implementations ────────────────────────────
    tool_ctx = {"user_id": student_id, "db": db}

    # ── Guardrail 3 & 5: Initialize trackers ──────────────────────────────
    sub_call_tracker = SubCallTracker()
    failed_tools = FailedToolTracker()

    # ── Tracking ──────────────────────────────────────────────────────────
    tools_used: list[str] = []
    tool_calls_log: list[dict] = []
    collected_graphs: list[dict] = []
    tool_results_data: dict[str, dict] = {}

    # ── 4. The Loop ───────────────────────────────────────────────────────
    for iteration in range(1, MAX_ITERATIONS + 1):
        logger.info(f"ReAct loop — iteration {iteration}")

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=memory.get_messages(),
                tools=TOOL_SCHEMAS,
                tool_choice="auto",
                temperature=0.3,
                max_tokens=3000,
            )
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return _build_return(
                "I'm having trouble thinking right now. Can you try again?",
                iteration, tools_used, tool_calls_log, collected_graphs,
                selected_mode, tool_results_data,
                validation_flags=["api_error"],
            )

        choice = response.choices[0]

        # ── Case 1: Agent is done — final text response ──────────────
        if choice.finish_reason == "stop" or not choice.message.tool_calls:
            final_text = choice.message.content or ""

            # ── Guardrail 4: Validate response ────────────────────────
            validation = validate_response(final_text, selected_mode)
            final_text = validation["corrected_text"]

            logger.info(f"ReAct loop — done after {iteration} iteration(s)")
            return _build_return(
                final_text, iteration, tools_used, tool_calls_log,
                collected_graphs, selected_mode, tool_results_data,
                validation_flags=validation["flags"],
            )

        # ── Case 2: Agent wants to use tools ─────────────────────────
        memory.add_tool_call(choice.message.model_dump())

        for tool_call in choice.message.tool_calls:
            fn_name = tool_call.function.name
            try:
                fn_args = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                fn_args = {}

            logger.info(f"ReAct loop — calling tool: {fn_name}({fn_args})")
            tools_used.append(fn_name)

            # ── Guardrail 5: Check if tool already failed ─────────────
            if failed_tools.has_failed(fn_name):
                result_str = failed_tools.get_block_message(fn_name)
                logger.info(f"ReAct loop — blocked retry of failed tool: {fn_name}")

            # ── Guardrail 3: Check sub-call limit ─────────────────────
            elif not sub_call_tracker.can_call(fn_name):
                result_str = json.dumps({
                    "error": "Sub-call limit reached for this request.",
                    "instruction": "Respond to the student using the information you already have.",
                })
                logger.info(f"ReAct loop — sub-call limit blocked: {fn_name}")

            else:
                # Execute the real tool
                result_str = execute_tool(fn_name, fn_args, **tool_ctx)
                sub_call_tracker.record_call(fn_name)

                # ── Guardrail 5: Check if tool returned an error ──────
                try:
                    parsed = json.loads(result_str)
                    if "error" in parsed:
                        failed_tools.mark_failed(fn_name)
                        result_str = wrap_tool_error(fn_name, result_str)
                        logger.warning(f"ReAct loop — tool failed: {fn_name}")
                    else:
                        tool_results_data[fn_name] = parsed
                except json.JSONDecodeError:
                    pass

            # Log for transparency
            tool_calls_log.append({
                "tool": fn_name,
                "args": fn_args,
                "result_preview": result_str[:200],
                "iteration": iteration,
            })

            # Collect graphs if the tool generated one
            if fn_name == "generate_graph":
                try:
                    result_data = json.loads(result_str)
                    if result_data.get("success") and result_data.get("image_base64"):
                        collected_graphs.append({
                            "graph_type": fn_args.get("graph_type"),
                            "data": fn_args.get("data"),
                            "image_base64": result_data["image_base64"],
                        })
                except json.JSONDecodeError:
                    pass

            # Feed the tool result back into short-term memory
            memory.add_tool_result(tool_call.id, result_str)

    # ── Safety: hit max iterations, force a final response ────────────────
    logger.warning(f"ReAct loop — hit max iterations ({MAX_ITERATIONS})")

    msgs = memory.get_messages()
    msgs.append({
        "role": "user",
        "content": "(System: You've used all available tool calls. Please give your final response to the student now.)",
    })

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=msgs,
            temperature=0.3,
            max_tokens=3000,
        )
        final_text = response.choices[0].message.content or ""
    except Exception:
        final_text = "I've been thinking about this for a while. Let me give you what I have so far."

    # Validate the forced response too
    validation = validate_response(final_text, selected_mode)
    final_text = validation["corrected_text"]

    return _build_return(
        final_text, MAX_ITERATIONS, tools_used, tool_calls_log,
        collected_graphs, selected_mode, tool_results_data,
        validation_flags=validation["flags"] + ["max_iterations_reached"],
    )


# A request is considered a "problem" (vs a follow-up) if the agent used
# tools that indicate it was working on math content, not just chatting.
PROBLEM_INDICATORS = {"get_hint_strategy", "generate_graph"}


def _build_return(
    message: str,
    iterations: int,
    tools_used: list[str],
    tool_calls_log: list[dict],
    graphs: list[dict],
    selected_mode: str | None,
    tool_results_data: dict,
    validation_flags: list[str] | None = None,
) -> dict:
    """Build the standardized return dict."""
    is_problem = bool(PROBLEM_INDICATORS & set(tools_used))

    return {
        "message": message,
        "iterations": iterations,
        "tools_used": tools_used,
        "tool_calls_made": tool_calls_log,
        "graphs": graphs,
        "mode_used": selected_mode or "agent_determined",
        "mode_source": "student_selected" if selected_mode else "agent_determined",
        "assessment": _extract_assessment(tool_results_data),
        "is_problem": is_problem,
        "validation_flags": validation_flags or [],
    }
