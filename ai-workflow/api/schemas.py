"""
schemas.py
Pydantic request and response models for the tutoring API.

Responsibility:
    Defines the shape of data coming in from the student (TutorRequest)
    and going back out (TutorResponse).
    These models are the contract between the client and the API.

Architecture:
    FastAPI validates all incoming requests against TutorRequest automatically.
    The router uses TutorResponse as the response_model to enforce output shape.
"""

from pydantic import BaseModel
from typing import Optional


class TutorRequest(BaseModel):
    """
    Incoming request from a student.

    Fields:
        student_input  The student's question or answer as raw text.
        subject        The subject area (e.g. "math"). Defaults to "math" if omitted.
        mode           The tutoring mode (e.g. "explain", "hint", "check"). Optional for now.
    """
    student_input: str
    subject: Optional[str] = "math"
    mode: Optional[str] = None


class TutorResponse(BaseModel):
    """
    Outgoing response returned to the student.

    Fields:
        subject   The subject that handled this request.
        response  The tutoring response text.
    """
    subject: str
    response: str
