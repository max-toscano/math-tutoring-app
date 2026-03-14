"""
models.py
SQLAlchemy ORM models mapped to Supabase PostgreSQL tables.
Tables are created via Supabase migrations — these models are read/write mappings only.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Text, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from db.database import Base


class Profile(Base):
    """Maps to the 'profiles' table — managed by Supabase Auth trigger."""
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True)
    display_name = Column(Text, nullable=True)
    grade_level = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)


class TutoringSession(Base):
    __tablename__ = "tutoring_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(Text, nullable=False)
    preview = Column(Text, nullable=True)
    subject = Column(Text, default="math")
    mode = Column(Text, nullable=True)
    photo_url = Column(Text, nullable=True)
    analysis = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))


class SessionMessage(Base):
    __tablename__ = "session_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("tutoring_sessions.id", ondelete="CASCADE"), nullable=False)
    role = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(Text, nullable=True)
    sort_order = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))


class Interaction(Base):
    """Every tutoring Q&A exchange. Core analytics table for progress tracking."""
    __tablename__ = "interactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    subject = Column(Text, nullable=False)
    topic = Column(Text, nullable=True)
    mode = Column(Text, nullable=False)
    student_input = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=True)
    mistake_type = Column(Text, nullable=True)
    difficulty = Column(Text, nullable=True)
    concepts = Column(JSONB, default=[])
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))


class SavedItem(Base):
    """Saved math problem analysis from photo scans."""
    __tablename__ = "saved_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    image_url = Column(Text, nullable=False)
    analysis = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
