"""
router.py
FastAPI router — the HTTP interface for the tutoring system.

Responsibility:
    Receives HTTP requests, passes student input to the tutor engine,
    and returns structured responses. Contains NO tutoring logic.

Architecture:
    router.py → tutor_engine.py → tutoring/subjects/math/
"""

from fastapi import APIRouter
from .schemas import TutorRequest, TutorResponse
from tutoring.orchestrator.tutor_engine import generate_tutoring_response

router = APIRouter(tags=["tutor"])


@router.post("/tutor/respond", response_model=TutorResponse)
async def tutor_respond(request: TutorRequest) -> TutorResponse:
    """
    Accept a student input and return a tutoring response.

    The router delegates all logic to the tutor engine.
    Subject defaults to 'math' until multi-subject routing is built.
    """
    result = generate_tutoring_response(
        student_input=request.student_input,
        requested_subject=request.subject,
        requested_mode=request.mode,
    )

    return TutorResponse(
        subject=result["subject"],
        response=result["response"],
    )


# TEMPORARY — kept for quick verification that the math module is reachable.
# Remove once /tutor/respond is confirmed working end-to-end.
@router.post("/tutor/math/rules")
def get_math_subject_rules() -> dict:
    """Return the core teaching rules for the math subject."""
    from tutoring.subjects.math import get_rules
    return {
        "subject": "math",
        "rules": get_rules(),
    }
