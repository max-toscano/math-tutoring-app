"""
schemas.py
Pydantic request/response models for all API endpoints.
"""

from pydantic import BaseModel
from typing import Optional


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

class RegisterRequest(BaseModel):
    display_name: Optional[str] = None
    email: Optional[str] = None
    device_id: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    display_name: Optional[str]
    email: Optional[str]


# ---------------------------------------------------------------------------
# Tutoring
# ---------------------------------------------------------------------------

VALID_SUBJECTS = {"math", "chemistry", "physics", "biology"}
VALID_MODES = {"direct", "socratic", "hint", "check_work"}

class TutorRequest(BaseModel):
    user_id: str
    student_input: str
    subject: str = "math"
    mode: str = "direct"
    image_base64: Optional[str] = None

class Assessment(BaseModel):
    is_correct: Optional[bool] = None
    mistake_type: Optional[str] = None
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    concepts: list[str] = []

class TutorResponse(BaseModel):
    subject: str
    mode: str
    response_text: str
    assessment: Assessment


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
    user_id: str
    subject: Optional[str] = None
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    problem: Optional[str] = None
    answer: Optional[str] = None
    steps: Optional[str] = None       # JSON string
    concepts: Optional[str] = None     # JSON string
    source: str = "scan"
    image_uri: Optional[str] = None

class SavedItemResponse(BaseModel):
    id: str
    subject: Optional[str]
    topic: Optional[str]
    difficulty: Optional[str]
    problem: Optional[str]
    answer: Optional[str]
    steps: Optional[str]
    concepts: Optional[str]
    source: str
    image_uri: Optional[str]
    created_at: str
