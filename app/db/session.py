"""
db/session.py
Database connection and session management.
Connects to Supabase PostgreSQL via SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL) if DATABASE_URL else None

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
) if engine else None


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency — yields a DB session and closes it after the request."""
    if not SessionLocal:
        raise RuntimeError("DATABASE_URL not configured")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
