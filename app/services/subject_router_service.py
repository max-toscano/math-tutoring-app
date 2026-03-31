"""
services/subject_router_service.py
Route requests to the correct subject engine.

Math-only for now. When other subjects are added (physics, chemistry),
this service determines which engine handles the request.
"""

from app.guardrails.policy import ALLOWED_SUBJECTS


class SubjectRouterService:
    """Route to the correct subject engine based on detected topic."""

    def route(self, topic_info: dict | None = None) -> str:
        """
        Determine which subject engine should handle this request.

        Args:
            topic_info: Optional topic detection result from TopicRetriever.

        Returns:
            Subject string (currently always "math").
        """
        if topic_info:
            subject = topic_info.get("subject", "math")
            if subject in ALLOWED_SUBJECTS:
                return subject

        # Default to math — it's the only subject for now
        return "math"
