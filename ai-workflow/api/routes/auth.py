"""
auth.py
Profile endpoint — auth is handled by Supabase on the frontend.
The backend just validates the JWT and returns the user's profile.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Profile
from api.auth_middleware import get_current_user_id

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
def get_me(user_id: UUID = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """Return the authenticated user's profile."""
    profile = db.query(Profile).filter(Profile.id == user_id).first()
    if not profile:
        raise HTTPException(404, "Profile not found")
    return {
        "id": str(profile.id),
        "display_name": profile.display_name,
        "grade_level": profile.grade_level,
    }
