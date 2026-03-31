"""
subjects/math/engine.py
The math tutoring engine.

This is where the LLM gets called with tools. The engine:
  - Builds the math-specific system prompt
  - Provides the math tools (symbolic, numerical, linear algebra, graphing)
  - Runs the LLM with tool-calling in a loop
  - Returns structured output

The engine does NOT coordinate the overall flow — that's the orchestrator's job.
The engine does NOT load memory or check guardrails — those happen before it runs.
The engine ONLY handles: build prompt → call LLM with tools → return result.
"""

import re
import json
import logging
from typing import Any


def _strip_base64(text: str) -> str:
    """Remove any base64 image data or raw data arrays from the response text."""
    # Strip markdown images with base64: ![...](data:image/png;base64,...)
    text = re.sub(r'!\[[^\]]*\]\(data:image[^)]+\)', '[Graph displayed above]', text)
    # Strip raw base64 blocks (50+ chars of base64 alphabet)
    text = re.sub(r'[A-Za-z0-9+/=]{50,}', '', text)
    # Strip JSON arrays of numbers/objects that leaked (e.g. [{"x": 1, "y": 2}, ...])
    text = re.sub(r'\[\s*\{["\']x["\']\s*:\s*[\d.-]+.*?\}\s*(?:,\s*\{["\']x["\']\s*:\s*[\d.-]+.*?\}\s*){2,}\]', '[data table computed]', text, flags=re.DOTALL)
    # Strip raw number arrays [1.0, 2.0, 3.0, ...]
    text = re.sub(r'\[\s*-?\d+\.?\d*\s*(?:,\s*-?\d+\.?\d*\s*){5,}\]', '[numerical data]', text)
    # Clean up leftover empty lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def _clean_tool_result(tool_name: str, result: str, collected_graphs: list) -> str:
    """
    Clean tool results before feeding back to the LLM.

    The LLM only needs summaries, not raw data arrays. Stripping large
    payloads prevents the LLM from dumping raw numbers into its response.

    - graphing: strip base64 image, keep success message
    - numerical_math: strip data arrays (tables, rectangles), keep summary
    - linear_algebra: strip large matrix results if needed
    - symbolic_math: keep as-is (results are small strings)
    """
    try:
        parsed = json.loads(result) if isinstance(result, str) else result
        if not isinstance(parsed, dict):
            return result

        # Check for errors — pass through as-is
        if parsed.get("error"):
            return result

        if tool_name == "graphing":
            if parsed.get("success"):
                collected_graphs.append(parsed)
                # Tell the LLM the graph is ready — don't include any graph data
                desmos = parsed.get("desmos", {})
                expr_count = len(desmos.get("expressions", []))
                return json.dumps({
                    "success": True,
                    "graph_type": parsed.get("graph_type"),
                    "expressions_plotted": expr_count,
                    "message": "Interactive graph generated and will be displayed to the student automatically. Reference it naturally in your response. Do NOT include any LaTeX expressions, coordinates, or graph data in your text."
                })

        elif tool_name == "numerical_math":
            operation = parsed.get("operation", "")

            if operation == "function_table":
                # Strip the full table, just tell LLM how many points
                table = parsed.get("table", [])
                return json.dumps({
                    "input": parsed.get("input"),
                    "operation": operation,
                    "points_computed": len(table),
                    "x_range": [table[0]["x"], table[-1]["x"]] if table else [],
                    "y_range": [min(p["y"] for p in table), max(p["y"] for p in table)] if table else [],
                    "message": "Function table computed. Use the x/y range to describe the behavior. Do NOT list individual data points.",
                    "error": None,
                })

            elif operation == "riemann_sum":
                # Strip rectangles array, keep the total
                return json.dumps({
                    "input": parsed.get("input"),
                    "operation": operation,
                    "method": parsed.get("method"),
                    "n": parsed.get("n"),
                    "a": parsed.get("a"),
                    "b": parsed.get("b"),
                    "total_area": parsed.get("total_area"),
                    "dx": parsed.get("dx"),
                    "message": "Riemann sum computed. Report the total area. Do NOT list individual rectangles.",
                    "error": None,
                })

            elif operation == "newtons_method":
                # Strip iteration details, keep the root
                iterations = parsed.get("iterations", [])
                return json.dumps({
                    "input": parsed.get("input"),
                    "operation": operation,
                    "root": parsed.get("root"),
                    "converged": parsed.get("converged"),
                    "iterations_count": len(iterations),
                    "message": "Root found. Report the root value. Do NOT list individual iterations.",
                    "error": None,
                })

        elif tool_name == "linear_algebra":
            operation = parsed.get("operation", "")

            if operation == "rref":
                # Keep the result matrix but add instruction
                parsed["message"] = "RREF computed. Show the result matrix cleanly. Do NOT dump raw arrays."
                return json.dumps(parsed)

        # Default: return as-is for small results (symbolic_math, simple evaluations)
        return result

    except (json.JSONDecodeError, TypeError, KeyError):
        return result


from app.llm.model import get_llm
from app.subjects.base.engine import BaseEngine
from app.subjects.math.prompts import build_math_system_prompt
from app.tools.math.symbolic_math import symbolic_math
from app.tools.math.numerical_math import numerical_math
from app.tools.math.linear_algebra import linear_algebra
from app.tools.math.graphing import graphing
from app.tools.math.web_search import math_web_search

logger = logging.getLogger(__name__)

MAX_TOOL_ITERATIONS = 6


class MathEngine(BaseEngine):
    """Math-specific tutoring engine with computational tools."""

    def get_tools(self) -> list:
        """Return the math tools available to the LLM."""
        return [symbolic_math, numerical_math, linear_algebra, graphing, math_web_search]

    def get_system_prompt(
        self,
        mode_instruction: str,
        student_context: str,
        rag_context: str,
        memory_context: str,
    ) -> str:
        """Build the math tutoring system prompt."""
        return build_math_system_prompt(
            mode_instruction=mode_instruction,
            student_context=student_context,
            rag_context=rag_context,
            memory_context=memory_context,
        )

    async def run(
        self,
        message: str,
        mode: str,
        mode_instruction: str,
        student_context: str,
        session_context: str,
        rag_context: str,
        memory_context: str,
        conversation_history: list[dict] | None = None,
        image_base64: str | None = None,
    ) -> dict:
        """
        Run the math engine for a single student message.

        Calls the LLM with math tools in a loop until it produces
        a final response or hits the iteration limit.
        """

        # ── Build system prompt ───────────────────────────────────────
        system_prompt = self.get_system_prompt(
            mode_instruction=mode_instruction,
            student_context=student_context,
            rag_context=rag_context,
            memory_context=memory_context,
        )

        # ── Build messages ────────────────────────────────────────────
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"[Session: {session_context}]"},
        ]

        # Add conversation history
        if conversation_history:
            for msg in conversation_history:
                messages.append({"role": msg["role"], "content": msg["content"]})

        # Add current message (with optional image)
        if image_base64:
            messages.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": message},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}},
                ],
            })
        else:
            messages.append({"role": "user", "content": message})

        # ── Get LLM with tools bound ─────────────────────────────────
        llm = get_llm()
        tools = self.get_tools()
        llm_with_tools = llm.bind_tools(tools)

        # ── Tool loop ─────────────────────────────────────────────────
        tools_used: list[str] = []
        collected_graphs: list[dict] = []
        detected_topic: str | None = None

        for iteration in range(1, MAX_TOOL_ITERATIONS + 1):
            logger.info(f"MathEngine — iteration {iteration}")

            response = llm_with_tools.invoke(messages)

            # Check if LLM wants to call tools
            if not response.tool_calls:
                # Done — final response (strip any leaked base64)
                return {
                    "response": _strip_base64(response.content),
                    "subject": "math",
                    "topic": detected_topic,
                    "mode": mode,
                    "tools_used": tools_used,
                    "graphs": collected_graphs,
                    "iterations": iteration,
                }

            # Process tool calls
            messages.append(response)

            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                logger.info(f"MathEngine — calling tool: {tool_name}")
                tools_used.append(tool_name)

                # Execute the tool
                tool_map = {t.name: t for t in tools}
                if tool_name in tool_map:
                    try:
                        result = tool_map[tool_name].invoke(tool_args)
                    except Exception as e:
                        result = json.dumps({"error": str(e)})
                else:
                    result = json.dumps({"error": f"Unknown tool: {tool_name}"})

                # Clean tool results before feeding back to LLM
                # Strip large data (base64, arrays, tables) — LLM only needs summaries
                llm_result = _clean_tool_result(tool_name, result, collected_graphs)

                # Add tool result to messages
                from langchain_core.messages import ToolMessage
                messages.append(ToolMessage(content=str(llm_result), tool_call_id=tool_call["id"]))

        # ── Hit max iterations — force a text response ────────────────
        logger.warning(f"MathEngine — hit max iterations ({MAX_TOOL_ITERATIONS})")
        messages.append({"role": "user", "content": "(Please give your final response now.)"})
        response = get_llm().invoke(messages)

        return {
            "response": _strip_base64(response.content),
            "subject": "math",
            "topic": detected_topic,
            "mode": mode,
            "tools_used": tools_used,
            "graphs": collected_graphs,
            "iterations": MAX_TOOL_ITERATIONS,
        }
