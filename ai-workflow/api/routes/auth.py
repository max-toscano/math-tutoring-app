"""
auth.py
Minimal user registration and login.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import User
from api.schemas import RegisterRequest, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """Create a new user. Accepts display_name, email, or device_id."""
    if req.email:
        existing = db.query(User).filter(User.email == req.email).first()
        if existing:
            raise HTTPException(400, "Email already registered")

    if req.device_id:
        existing = db.query(User).filter(User.device_id == req.device_id).first()
        if existing:
            return UserResponse(id=existing.id, display_name=existing.display_name, email=existing.email)

    user = User(
        display_name=req.display_name,
        email=req.email,
        device_id=req.device_id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse(id=user.id, display_name=user.display_name, email=user.email)


@router.post("/login", response_model=UserResponse)
def login(req: RegisterRequest, db: Session = Depends(get_db)):
    """Look up a user by email or device_id."""
    user = None
    if req.email:
        user = db.query(User).filter(User.email == req.email).first()
    elif req.device_id:
        user = db.query(User).filter(User.device_id == req.device_id).first()

    if not user:
        raise HTTPException(404, "User not found")

    return UserResponse(id=user.id, display_name=user.display_name, email=user.email)
