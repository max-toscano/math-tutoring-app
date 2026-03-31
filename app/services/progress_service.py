"""
services/progress_service.py
Track and query student learning progress.

Reads from student_profiles to provide progress data
for the orchestrator, API responses, and frontend.
"""

from sqlalchemy import text
from sqlalchemy.orm import Session as DBSession


class ProgressService:
    """Track student learning progress."""

    def __init__(self, db: DBSession):
        self.db = db

    async def get_summary(self, student_id: str) -> dict:
        """
        Get an overall progress summary for a student.

        Returns:
            {
                "total_sessions": int,
                "total_problems": int,
                "success_rate": float,
                "longest_streak": int,
                "topics_practiced": int,
                "weak_count": int,
            }
        """
        row = self.db.execute(
            text("""
                SELECT total_sessions, total_problems_attempted,
                       overall_success_rate, longest_streak,
                       topic_mastery, weak_areas
                FROM student_profiles WHERE student_id = :sid
            """),
            {"sid": student_id},
        ).mappings().first()

        if not row:
            return {
                "total_sessions": 0,
                "total_problems": 0,
                "success_rate": 0.0,
                "longest_streak": 0,
                "topics_practiced": 0,
                "weak_count": 0,
            }

        topic_mastery = row["topic_mastery"] or {}
        weak_areas = row["weak_areas"] or []

        return {
            "total_sessions": row["total_sessions"] or 0,
            "total_problems": row["total_problems_attempted"] or 0,
            "success_rate": row["overall_success_rate"] or 0.0,
            "longest_streak": row["longest_streak"] or 0,
            "topics_practiced": len(topic_mastery),
            "weak_count": len(weak_areas),
        }

    async def get_topic_mastery(self, student_id: str) -> dict:
        """Get per-topic mastery breakdown."""
        row = self.db.execute(
            text("SELECT topic_mastery FROM student_profiles WHERE student_id = :sid"),
            {"sid": student_id},
        ).mappings().first()

        return row["topic_mastery"] if row else {}
