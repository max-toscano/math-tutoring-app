"""
schemas.py
Pydantic request/response models for all API endpoints.
user_id is no longer in request bodies — it comes from the JWT token.
"""

from pydantic import BaseModel
from typing import Optional, Any


# ---------------------------------------------------------------------------
# Tutoring
# ---------------------------------------------------------------------------

VALID_SUBJECTS = {"math", "chemistry", "physics", "biology"}
VALID_MODES = {"direct", "socratic", "hint", "check_work"}

class Message(BaseModel):
    role: str
    content: str

class TutorRequest(BaseModel):
    student_input: str
    subject: str = "math"
    mode: str = "direct"
    image_base64: Optional[str] = None
    conversation_history: Optional[list[Message]] = None

class Assessment(BaseModel):
    is_correct: Optional[bool] = None
    mistake_type: Optional[str] = None
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    concepts: list[str] = []

class TutorResponse(BaseModel):
    subject: str
    mode: str
    response: str = ""
    response_text: Optional[str] = None
    assessment: Optional[Assessment] = None
    conversation_history: list[Message] = []


# ---------------------------------------------------------------------------
# Progress / Performance
# ---------------------------------------------------------------------------

class SubjectSummary(BaseModel):
    subject: str
    total: int
    correct: int
    accuracy: float

class TopicBreakdown(BaseModel):
    topic: str
    total: int
    correct: int
    accuracy: float

class WeakArea(BaseModel):
    subject: str
    topic: str
    attempts: int
    accuracy: float

class MistakeCount(BaseModel):
    mistake_type: str
    count: int

class ProgressSummaryResponse(BaseModel):
    subjects: list[SubjectSummary]
    total_interactions: int
    weak_areas: list[WeakArea]

class SubjectDetailResponse(BaseModel):
    subject: str
    overall_accuracy: float
    topics: list[TopicBreakdown]
    top_mistakes: list[MistakeCount]


# ---------------------------------------------------------------------------
# Saved Items
# ---------------------------------------------------------------------------

class SaveItemRequest(BaseModel):
    image_url: str
    analysis: dict[str, Any]

class SavedItemResponse(BaseModel):
    id: str
    image_url: str
    analysis: dict[str, Any]
    created_at: str
