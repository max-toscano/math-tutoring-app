"""
memory/retrieval.py
Retrieve relevant student memory for the current request.

Pulls weak areas and learning notes from student_profiles
to give the agent context about this student's patterns.
"""

from sqlalchemy import text
from sqlalchemy.orm import Session as DBSession


class MemoryRetriever:
    """Retrieve relevant past memory for a student's current question."""

    def __init__(self, db: DBSession):
        self.db = db

    async def retrieve_relevant(self, student_id: str, query: str) -> str:
        """
        Get student-specific context relevant to the current query.

        Pulls weak areas and learning notes from student_profiles.
        These help the agent know what patterns to watch for.

        Args:
            student_id: The student's ID.
            query: What the student is asking about.

        Returns:
            Formatted string with relevant memory, or empty string.
        """
        row = self.db.execute(
            text("SELECT weak_areas, learning_notes, topic_mastery FROM student_profiles WHERE student_id = :sid"),
            {"sid": student_id},
        ).mappings().first()

        if not row:
            return ""

        parts = []

        weak_areas = row["weak_areas"] or []
        if weak_areas:
            parts.append("**Known Weak Areas:** " + ", ".join(weak_areas))

        learning_notes = row["learning_notes"] or []
        if learning_notes:
            parts.append("**Learning Notes:** " + " | ".join(learning_notes))

        return "\n".join(parts)
