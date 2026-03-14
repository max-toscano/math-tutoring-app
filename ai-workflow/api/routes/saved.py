"""
saved.py
CRUD endpoints for saved math problem analysis items.
Saved items are now stored in Supabase with image_url and JSONB analysis.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import SavedItem
from api.auth_middleware import get_current_user_id
from api.schemas import SaveItemRequest, SavedItemResponse

router = APIRouter(prefix="/saved", tags=["saved"])


def _to_response(item: SavedItem) -> SavedItemResponse:
    return SavedItemResponse(
        id=str(item.id),
        image_url=item.image_url,
        analysis=item.analysis,
        created_at=item.created_at.isoformat(),
    )


@router.get("", response_model=list[SavedItemResponse])
def list_saved(user_id: UUID = Depends(get_current_user_id), db: Session = Depends(get_db)):
    """List all saved items for the authenticated user, newest first."""
    items = (
        db.query(SavedItem)
        .filter(SavedItem.user_id == user_id)
        .order_by(SavedItem.created_at.desc())
        .all()
    )
    return [_to_response(i) for i in items]


@router.post("", response_model=SavedItemResponse)
def save_item(
    req: SaveItemRequest,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Save a math problem analysis."""
    item = SavedItem(
        user_id=user_id,
        image_url=req.image_url,
        analysis=req.analysis,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return _to_response(item)


@router.delete("/{item_id}")
def delete_saved(
    item_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Delete a saved item by ID (only if owned by the authenticated user)."""
    item = db.query(SavedItem).filter(SavedItem.id == item_id, SavedItem.user_id == user_id).first()
    if not item:
        raise HTTPException(404, "Saved item not found")
    db.delete(item)
    db.commit()
    return {"deleted": str(item_id)}
