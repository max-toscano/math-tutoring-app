"""
services/session_service.py
Manage tutoring session lifecycle.

Wraps the memory layer's session functions into a service
the orchestrator calls for session start, load, and close.
"""

from sqlalchemy.orm import Session as DBSession
from app.memory.memory_manager import MemoryManager


class SessionService:
    """Manage session lifecycle for the orchestrator."""

    def __init__(self, memory: MemoryManager):
        self.memory = memory

    async def start_session(self, student_id: str) -> str:
        """Start a new session. Returns session_id."""
        return await self.memory.start_new_session(student_id)

    async def load_history(self, student_id: str, session_id: str, selected_mode: str | None = None) -> dict:
        """
        Load session context and student context.

        Returns:
            {"student_context": str, "session_context": str}
        """
        return await self.memory.load_context(student_id, session_id, selected_mode)

    async def save_turn(self, session_id: str, problem_result: dict) -> None:
        """Save a problem result to the session."""
        await self.memory.save_problem(session_id, problem_result)

    async def close_session(self, student_id: str, session_id: str) -> dict:
        """Close session, generate summary, update mastery."""
        return await self.memory.close_and_update(student_id, session_id)
