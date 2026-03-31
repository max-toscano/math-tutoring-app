"""
orchestrators/tutor_orchestrator.py
The main workflow coordinator.

This is the brain that calls everything in the right order.
It does NOT contain logic itself — it delegates to the right modules.

Flow:
  1. Input guardrails
  2. Load session history
  3. Retrieve relevant memory
  4. Detect topic (OpenStax RAG)
  5. Retrieve grounded teaching context (OpenStax RAG)
  6. Resolve tutoring mode
  7. Run the subject engine (MathEngine)
  8. Output guardrails
  9. Save session + memory + progress
  10. Return response
"""

import logging
from sqlalchemy.orm import Session as DBSession

from app.guardrails.input_guardrails import InputGuardrails
from app.guardrails.output_guardrails import OutputGuardrails
from app.memory.memory_manager import MemoryManager
from app.memory.retrieval import MemoryRetriever
from app.services.session_service import SessionService
from app.services.subject_router_service import SubjectRouterService
from app.services.mode_service import ModeService
from app.services.progress_service import ProgressService
from app.rag.retrieval.topic_retriever import TopicRetriever
from app.rag.retrieval.openstax_retriever import OpenStaxRetriever
from app.tools.math.web_search import search_web
from app.subjects.math.engine import MathEngine

logger = logging.getLogger(__name__)


class TutorOrchestrator:
    """Coordinate the full tutoring request from start to finish."""

    def __init__(self, db: DBSession):
        self.db = db

        # Initialize all modules
        self.input_guardrails = InputGuardrails()
        self.output_guardrails = OutputGuardrails()
        self.memory = MemoryManager(db)
        self.memory_retriever = MemoryRetriever(db)
        self.session_service = SessionService(self.memory)
        self.subject_router = SubjectRouterService()
        self.mode_service = ModeService()
        self.progress_service = ProgressService(db)

        # RAG components (SQL-based, no vectors)
        self.topic_retriever = TopicRetriever(db)
        self.openstax_retriever = OpenStaxRetriever(db)

        # Subject engines
        self.math_engine = MathEngine()

    async def handle_message(
        self,
        student_id: str,
        session_id: str,
        message: str,
        selected_mode: str | None = None,
        image_base64: str | None = None,
        conversation_history: list[dict] | None = None,
    ) -> dict:
        """
        Process a single student message through the full pipeline.

        Returns:
            {
                "response": str,
                "subject": str,
                "topic": str | None,
                "mode": str,
                "mode_source": str,
                "tools_used": list[str],
                "graphs": list[dict],
                "validation_flags": list[str],
            }
        """

        # ── 1. Input guardrails ───────────────────────────────────────
        input_check = await self.input_guardrails.validate(message, image_base64)
        if not input_check["allowed"]:
            logger.info(f"Input guardrail blocked: {input_check['reason']}")
            return {
                "response": input_check["redirect_message"],
                "subject": None,
                "topic": None,
                "mode": None,
                "mode_source": None,
                "tools_used": [],
                "graphs": [],
                "validation_flags": [f"input_blocked:{input_check['reason']}"],
            }

        # ── 2. Load session history + student context ─────────────────
        context = await self.session_service.load_history(
            student_id, session_id, selected_mode
        )
        student_context = context["student_context"]
        session_context = context["session_context"]

        # ── 3. Retrieve relevant memory ───────────────────────────────
        memory_context = await self.memory_retriever.retrieve_relevant(
            student_id, message
        )

        # ── 4. Detect topic via OpenStax RAG ──────────────────────────
        topic_info = self.topic_retriever.detect_topic(message)
        detected_topic = topic_info.get("topic")
        logger.info(f"Topic detected: {detected_topic} (confidence: {topic_info.get('confidence', 0):.2f})")

        # ── 5. Retrieve grounded context via web search ────────────────
        # Searches for OpenStax / educational content on the topic
        # Pulls fresh, real textbook-quality material every time
        rag_context = ""
        search_query = f"OpenStax {detected_topic.replace('_', ' ')} math explanation formulas examples" if detected_topic and detected_topic != "unknown" else f"math tutorial {message[:150]}"
        try:
            web_result = search_web(search_query)
            if web_result.get("result") and not web_result.get("error"):
                rag_context = f"## Reference Material\n\n{web_result['result'][:2000]}"
                # Include source citations if available
                annotations = web_result.get("annotations", [])
                if annotations:
                    sources = "\n".join(f"- [{a.get('title', 'Source')}]({a.get('url', '')})" for a in annotations[:3])
                    rag_context += f"\n\n**Sources:**\n{sources}"
                logger.info(f"Web search grounding: {len(web_result['result'])} chars for '{search_query[:50]}...'")
        except Exception as e:
            logger.warning(f"Web search for grounding failed: {e}")
            # AI still works without grounding — just uses its own knowledge

        # ── 6. Resolve tutoring mode ──────────────────────────────────
        resolved_mode = self.mode_service.resolve_mode(
            selected_mode=selected_mode,
            preferred_mode=None,  # Could extract from student_context
        )
        mode_instruction = self.mode_service.get_mode_instruction(resolved_mode)
        mode_source = self.mode_service.get_mode_source(selected_mode, resolved_mode)

        # ── 7. Route to subject engine ────────────────────────────────
        subject = self.subject_router.route(topic_info)

        # ── 8. Run the engine ─────────────────────────────────────────
        if subject == "math":
            engine_result = await self.math_engine.run(
                message=message,
                mode=resolved_mode,
                mode_instruction=mode_instruction,
                student_context=student_context,
                session_context=session_context,
                rag_context=rag_context,
                memory_context=memory_context,
                conversation_history=conversation_history,
                image_base64=image_base64,
            )
        else:
            engine_result = {
                "response": "I can only help with math right now. What math topic are you working on?",
                "subject": subject,
                "topic": None,
                "mode": resolved_mode,
                "tools_used": [],
                "graphs": [],
            }

        # ── 9. Output guardrails ──────────────────────────────────────
        validation = self.output_guardrails.validate(
            engine_result["response"],
            resolved_mode,
        )
        final_response = validation["corrected_text"]

        # ── 10. Save session ──────────────────────────────────────────
        try:
            await self.session_service.save_turn(session_id, {
                "expression": message[:200],
                "type": detected_topic or "",
                "result": "unassessed",
                "mode_used": resolved_mode,
                "mode_source": mode_source,
                "hints_used": 0,
                "time_seconds": None,
                "error_types": [],
                "iterations_used": engine_result.get("iterations", 0),
            })
        except Exception as e:
            logger.error(f"Failed to save session turn: {e}")

        # ── 11. Generate follow-up suggestions ────────────────────────
        suggestions = _generate_suggestions(detected_topic, resolved_mode, engine_result.get("tools_used", []))

        # ── 12. Return structured response ────────────────────────────
        return {
            "response": final_response,
            "subject": engine_result.get("subject", "math"),
            "topic": detected_topic,
            "mode": resolved_mode,
            "mode_source": mode_source,
            "tools_used": engine_result.get("tools_used", []),
            "graphs": engine_result.get("graphs", []),
            "validation_flags": validation.get("flags", []),
            "suggestions": suggestions,
        }


def _generate_suggestions(topic: str | None, mode: str, tools_used: list[str]) -> list[str]:
    """Generate context-aware follow-up suggestion chips."""
    suggestions = []

    if mode == "explain":
        suggestions.append("Show me an example")
        suggestions.append("Why does this work?")
        if topic:
            suggestions.append(f"Practice {topic.replace('_', ' ')}")

    elif mode == "guide_me":
        suggestions.append("Next step")
        suggestions.append("I'm stuck on this step")
        suggestions.append("Can you explain why?")

    elif mode == "hint":
        suggestions.append("Another hint")
        suggestions.append("Just show me")
        suggestions.append("I think I got it")

    elif mode == "check_answer":
        suggestions.append("Show me the correct way")
        suggestions.append("Why is that wrong?")
        suggestions.append("Let me try again")

    else:  # auto
        suggestions.append("Explain this more")
        suggestions.append("Show me a graph")
        if topic:
            suggestions.append(f"Practice {topic.replace('_', ' ')}")
        else:
            suggestions.append("Give me a problem to try")

    # If graphing was used, don't suggest "show me a graph"
    if "graphing" in tools_used:
        suggestions = [s for s in suggestions if "graph" not in s.lower()]
        suggestions.append("Zoom in on that graph")

    return suggestions[:3]
