"""
saved.py
CRUD endpoints for saved homework and quiz items.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import SavedItem
from api.schemas import SaveItemRequest, SavedItemResponse

router = APIRouter(prefix="/saved", tags=["saved"])


def _to_response(item: SavedItem) -> SavedItemResponse:
    return SavedItemResponse(
        id=item.id,
        subject=item.subject,
        topic=item.topic,
        difficulty=item.difficulty,
        problem=item.problem,
        answer=item.answer,
        steps=item.steps,
        concepts=item.concepts,
        source=item.source,
        image_uri=item.image_uri,
        created_at=item.created_at.isoformat(),
    )


@router.get("", response_model=list[SavedItemResponse])
def list_saved(user_id: str = Query(...), db: Session = Depends(get_db)):
    """List all saved items for a user, newest first."""
    items = (
        db.query(SavedItem)
        .filter(SavedItem.user_id == user_id)
        .order_by(SavedItem.created_at.desc())
        .all()
    )
    return [_to_response(i) for i in items]


@router.post("", response_model=SavedItemResponse)
def save_item(req: SaveItemRequest, db: Session = Depends(get_db)):
    """Save a homework or quiz item."""
    item = SavedItem(
        user_id=req.user_id,
        subject=req.subject,
        topic=req.topic,
        difficulty=req.difficulty,
        problem=req.problem,
        answer=req.answer,
        steps=req.steps,
        concepts=req.concepts,
        source=req.source,
        image_uri=req.image_uri,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return _to_response(item)


@router.delete("/{item_id}")
def delete_saved(item_id: str, db: Session = Depends(get_db)):
    """Delete a saved item by ID."""
    item = db.query(SavedItem).filter(SavedItem.id == item_id).first()
    if not item:
        raise HTTPException(404, "Saved item not found")
    db.delete(item)
    db.commit()
    return {"deleted": item_id}
