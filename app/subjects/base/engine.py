"""
subjects/base/engine.py
Abstract base engine for all subject tutoring engines.

Defines the interface that every subject engine must implement.
The orchestrator calls the engine through this interface —
it doesn't need to know if it's math, physics, or chemistry.
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseEngine(ABC):
    """Abstract base class for subject-specific tutoring engines."""

    @abstractmethod
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
        Run the tutoring engine for a single student message.

        Args:
            message: What the student said.
            mode: Resolved mode (auto, explain, guide_me, hint, check_answer).
            mode_instruction: The prompt instruction text for the mode.
            student_context: Formatted student profile from long-term memory.
            session_context: Formatted session state from session memory.
            rag_context: Retrieved OpenStax content for grounding.
            memory_context: Relevant past interactions/weak areas.
            conversation_history: Prior messages in this session.
            image_base64: Optional image of student's work.

        Returns:
            {
                "response": str,          # The tutoring response text
                "subject": str,           # e.g. "math"
                "topic": str | None,      # detected topic
                "mode": str,              # mode used
                "tools_used": list[str],  # which tools were called
                "graphs": list[dict],     # any generated visualizations
            }
        """
        pass

    @abstractmethod
    def get_system_prompt(
        self,
        mode_instruction: str,
        student_context: str,
        rag_context: str,
        memory_context: str,
    ) -> str:
        """Build the system prompt for this subject engine."""
        pass

    @abstractmethod
    def get_tools(self) -> list:
        """Return the tools available to this engine."""
        pass
