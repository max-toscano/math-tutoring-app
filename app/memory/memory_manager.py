"""
memory/memory_manager.py
Main memory coordinator used by the orchestrator.

Wraps the existing long_term.py, session.py, and short_term.py
into a single interface the orchestrator can call.
"""

from sqlalchemy.orm import Session as DBSession

from app.memory.long_term import get_student_context, update_mastery
from app.memory.session import (
    start_session,
    get_session_context,
    save_problem_result,
    close_session,
)
from app.memory.short_term import ShortTermMemory


class MemoryManager:
    """Coordinate all three memory layers for the orchestrator."""

    def __init__(self, db: DBSession):
        self.db = db
        self.short_term = ShortTermMemory()

    async def load_context(
        self,
        student_id: str,
        session_id: str,
        selected_mode: str | None = None,
    ) -> dict:
        """
        Load all context needed before the engine runs.

        Returns:
            {
                "student_context": str,   # from student_profiles
                "session_context": str,   # from agent_sessions
            }
        """
        student_context = await get_student_context(student_id, self.db)
        session_context = await get_session_context(session_id, self.db, selected_mode)

        return {
            "student_context": student_context,
            "session_context": session_context,
        }

    async def save_problem(self, session_id: str, result: dict) -> None:
        """Save a problem result to the active session."""
        await save_problem_result(session_id, result, self.db)

    async def close_and_update(self, student_id: str, session_id: str) -> dict:
        """
        Close the session and update long-term mastery.
        Returns the session close data (summary, stats).
        """
        session_data = await close_session(session_id, self.db)
        if session_data:
            await update_mastery(student_id, session_data, self.db)
        return session_data or {}

    async def start_new_session(self, student_id: str) -> str:
        """Start a new session, returns session_id."""
        return await start_session(student_id, self.db)

    def get_short_term(self) -> ShortTermMemory:
        """Access the short-term memory for the current request."""
        return self.short_term
