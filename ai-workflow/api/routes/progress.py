"""
progress.py
Performance tracking endpoints. All metrics are computed queries
over the interactions table — no separate stats table needed.
"""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from db.database import get_db
from db.models import Interaction
from api.auth_middleware import get_current_user_id
from api.schemas import (
    ProgressSummaryResponse, SubjectSummary, WeakArea,
    SubjectDetailResponse, TopicBreakdown, MistakeCount,
)

router = APIRouter(prefix="/progress", tags=["progress"])

WEAK_AREA_THRESHOLD = 0.6
MIN_ATTEMPTS = 3


@router.get("/summary", response_model=ProgressSummaryResponse)
def get_summary(user_id: UUID = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Per-subject accuracy, total interactions, and weak areas."""

    # Per-subject accuracy
    rows = (
        db.query(
            Interaction.subject,
            func.count().label("total"),
            func.sum(case((Interaction.is_correct == True, 1), else_=0)).label("correct"),
        )
        .filter(Interaction.user_id == user_id, Interaction.is_correct.isnot(None))
        .group_by(Interaction.subject)
        .all()
    )

    subjects = [
        SubjectSummary(
            subject=r.subject,
            total=r.total,
            correct=r.correct,
            accuracy=round(r.correct / r.total * 100, 1) if r.total else 0,
        )
        for r in rows
    ]

    # Total interactions (including non-graded ones)
    total = db.query(func.count()).filter(Interaction.user_id == user_id).scalar()

    # Weak areas
    weak_rows = (
        db.query(
            Interaction.subject,
            Interaction.topic,
            func.count().label("attempts"),
            func.sum(case((Interaction.is_correct == True, 1), else_=0)).label("correct"),
        )
        .filter(Interaction.user_id == user_id, Interaction.is_correct.isnot(None))
        .group_by(Interaction.subject, Interaction.topic)
        .all()
    )

    weak_areas = [
        WeakArea(
            subject=r.subject,
            topic=r.topic or "general",
            attempts=r.attempts,
            accuracy=round(r.correct / r.attempts * 100, 1),
        )
        for r in weak_rows
        if r.attempts >= MIN_ATTEMPTS and (r.correct / r.attempts) < WEAK_AREA_THRESHOLD
    ]
    weak_areas.sort(key=lambda w: w.accuracy)

    return ProgressSummaryResponse(
        subjects=subjects,
        total_interactions=total,
        weak_areas=weak_areas,
    )


@router.get("/subject/{subject}", response_model=SubjectDetailResponse)
def get_subject_detail(
    subject: str,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Per-topic breakdown within a single subject."""

    # Per-topic accuracy
    rows = (
        db.query(
            Interaction.topic,
            func.count().label("total"),
            func.sum(case((Interaction.is_correct == True, 1), else_=0)).label("correct"),
        )
        .filter(
            Interaction.user_id == user_id,
            Interaction.subject == subject,
            Interaction.is_correct.isnot(None),
        )
        .group_by(Interaction.topic)
        .all()
    )

    topics = [
        TopicBreakdown(
            topic=r.topic or "general",
            total=r.total,
            correct=r.correct,
            accuracy=round(r.correct / r.total * 100, 1) if r.total else 0,
        )
        for r in rows
    ]
    topics.sort(key=lambda t: t.accuracy)

    # Overall accuracy for this subject
    total_correct = sum(t.correct for t in topics)
    total_attempts = sum(t.total for t in topics)
    overall = round(total_correct / total_attempts * 100, 1) if total_attempts else 0

    # Top mistake types in this subject
    mistake_rows = (
        db.query(
            Interaction.mistake_type,
            func.count().label("count"),
        )
        .filter(
            Interaction.user_id == user_id,
            Interaction.subject == subject,
            Interaction.mistake_type.isnot(None),
        )
        .group_by(Interaction.mistake_type)
        .order_by(func.count().desc())
        .limit(10)
        .all()
    )

    top_mistakes = [
        MistakeCount(mistake_type=r.mistake_type, count=r.count)
        for r in mistake_rows
    ]

    return SubjectDetailResponse(
        subject=subject,
        overall_accuracy=overall,
        topics=topics,
        top_mistakes=top_mistakes,
    )


@router.get("/weak-areas", response_model=list[WeakArea])
def get_weak_areas(user_id: UUID = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Topics where the student scores below 60% with at least 3 attempts."""

    rows = (
        db.query(
            Interaction.subject,
            Interaction.topic,
            func.count().label("attempts"),
            func.sum(case((Interaction.is_correct == True, 1), else_=0)).label("correct"),
        )
        .filter(Interaction.user_id == user_id, Interaction.is_correct.isnot(None))
        .group_by(Interaction.subject, Interaction.topic)
        .all()
    )

    weak = [
        WeakArea(
            subject=r.subject,
            topic=r.topic or "general",
            attempts=r.attempts,
            accuracy=round(r.correct / r.attempts * 100, 1),
        )
        for r in rows
        if r.attempts >= MIN_ATTEMPTS and (r.correct / r.attempts) < WEAK_AREA_THRESHOLD
    ]
    weak.sort(key=lambda w: w.accuracy)
    return weak
