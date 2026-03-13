"""
models.py
SQLAlchemy ORM models for users, interactions, and saved items.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Text, Boolean, DateTime, ForeignKey, Float
from db.database import Base


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Text, primary_key=True, default=_uuid)
    display_name = Column(Text, nullable=True)
    email = Column(Text, unique=True, nullable=True)
    device_id = Column(Text, unique=True, nullable=True)
    created_at = Column(DateTime, default=_now)


class Interaction(Base):
    """Every tutoring Q&A exchange. This is the core analytics table."""
    __tablename__ = "interactions"

    id = Column(Text, primary_key=True, default=_uuid)
    user_id = Column(Text, ForeignKey("users.id"), nullable=False)
    subject = Column(Text, nullable=False)          # "math", "chemistry", "physics"
    topic = Column(Text, nullable=True)              # AI-determined: "algebra", "stoichiometry"
    mode = Column(Text, nullable=False)              # "socratic", "hint", "direct", "check_work"
    student_input = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=True)      # null if not an answer-check
    mistake_type = Column(Text, nullable=True)       # "sign_error", "wrong_formula", etc.
    difficulty = Column(Text, nullable=True)          # "Easy", "Medium", "Hard"
    concepts = Column(Text, nullable=True)            # JSON array of concept strings
    created_at = Column(DateTime, default=_now)


class SavedItem(Base):
    """Homework or quiz problems the student saves while working."""
    __tablename__ = "saved_items"

    id = Column(Text, primary_key=True, default=_uuid)
    user_id = Column(Text, ForeignKey("users.id"), nullable=False)
    subject = Column(Text, nullable=True)
    topic = Column(Text, nullable=True)
    difficulty = Column(Text, nullable=True)
    problem = Column(Text, nullable=True)
    answer = Column(Text, nullable=True)
    steps = Column(Text, nullable=True)              # JSON array
    concepts = Column(Text, nullable=True)            # JSON array
    source = Column(Text, default="scan")            # "scan", "quiz", "learn"
    image_uri = Column(Text, nullable=True)
    created_at = Column(DateTime, default=_now)
