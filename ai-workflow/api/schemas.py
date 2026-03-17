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


# ---------------------------------------------------------------------------
# Learn (structured lessons)
# ---------------------------------------------------------------------------

class LessonRequest(BaseModel):
    subject: str          # slug, e.g. "calc-2"
    chapter: Optional[str] = None  # slug, e.g. "right-triangle-trig" — required for chaptered subjects, None for flat
    topic: str            # slug, e.g. "taylor-maclaurin"
    student_input: Optional[str] = None  # None on first message (AI introduces topic)
    conversation_history: Optional[list[Message]] = None


# --- Structured lesson response (phase-aware) ---

class QuizResultResponse(BaseModel):
    is_correct: bool
    explanation: str = ""
    running_score: Optional[dict[str, int]] = None  # {"correct": 2, "total": 3}
    concept_tested: Optional[str] = None

class QuizSummaryResponse(BaseModel):
    final_score: int
    passed: bool                        # app-validated, not AI's opinion
    missed_concepts: list[str] = []
    message: str = ""

class QuizOutcome(BaseModel):
    """Returned when a quiz is finalized (after question 5)."""
    score: int
    passed: bool
    new_phase: str
    new_status: str
    missed_concepts: list[str] = []

class LessonResponse(BaseModel):
    message: str                                     # AI's conversational message
    phase: Optional[str] = None                      # current phase after this response
    images: list[str] = []                           # image IDs referenced by AI
    quiz_result: Optional[QuizResultResponse] = None # per-question quiz feedback
    quiz_outcome: Optional[QuizOutcome] = None       # after all 5 questions
    conversation_history: list[Message] = []

    # Legacy compat — frontend can migrate gradually
    response_text: Optional[str] = None
    assessment: Optional[dict[str, Any]] = None


class TopicProgress(BaseModel):
    subject: str
    chapter: Optional[str] = None  # None for flat subjects (_default in DB)
    topic: str
    status: str           # not_started | in_progress | completed | failed_last_attempt
    phase: Optional[str] = None  # lesson | practice | quiz | review | done
    messages_count: int
    last_accessed_at: Optional[str] = None
