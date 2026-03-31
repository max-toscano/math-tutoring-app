"""
api/routes/chat.py
Chat endpoint — single entry point for all student interactions.

Three endpoints:
  POST /chat/start-session  → create a new session
  POST /chat/message        → send a message to the tutor
  POST /chat/close-session  → close the session and update mastery
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.db.session import get_db
from app.api.middleware.auth import get_current_student_id
from app.orchestrators.tutor_orchestrator import TutorOrchestrator
from app.memory.memory_manager import MemoryManager
from app.services.mode_service import VALID_MODES

router = APIRouter(prefix="/chat", tags=["chat"])


# ── Request / Response schemas ────────────────────────────────────────────

class StartSessionResponse(BaseModel):
    session_id: str

class MessageRequest(BaseModel):
    session_id: str
    message: str
    image_base64: Optional[str] = None
    selected_mode: Optional[str] = None
    conversation_history: Optional[list[dict]] = None

class DesmosExpression(BaseModel):
    latex: str
    color: Optional[str] = None
    lineStyle: Optional[str] = None
    label: Optional[str] = None
    fillOpacity: Optional[float] = None
    pointStyle: Optional[str] = None

class DesmosBounds(BaseModel):
    left: float = -10
    right: float = 10
    top: float = 10
    bottom: float = -10

class DesmosConfig(BaseModel):
    expressions: list[DesmosExpression] = []
    bounds: Optional[DesmosBounds] = None

class GraphOutput(BaseModel):
    graph_type: Optional[str] = None
    image_base64: Optional[str] = None
    desmos: Optional[DesmosConfig] = None

class MessageResponse(BaseModel):
    response: str
    subject: Optional[str] = None
    topic: Optional[str] = None
    mode: Optional[str] = None
    mode_source: Optional[str] = None
    tools_used: list[str] = []
    graphs: list[GraphOutput] = []
    validation_flags: list[str] = []
    suggestions: list[str] = []

class CloseSessionRequest(BaseModel):
    session_id: str

class CloseSessionResponse(BaseModel):
    session_summary: Optional[str] = None
    total_problems: int = 0
    success_rate: float = 0.0


# ── Endpoints ─────────────────────────────────────────────────────────────

@router.post("/start-session", response_model=StartSessionResponse)
async def start_session(
    student_id: str = Depends(get_current_student_id),
    db: Session = Depends(get_db),
):
    """Start a new tutoring session. Returns session_id for subsequent calls."""
    memory = MemoryManager(db)
    session_id = await memory.start_new_session(student_id)
    return StartSessionResponse(session_id=session_id)


@router.post("/message", response_model=MessageResponse)
async def send_message(
    req: MessageRequest,
    student_id: str = Depends(get_current_student_id),
    db: Session = Depends(get_db),
):
    """
    Send a message to the math tutor.

    The orchestrator handles the full pipeline:
    guardrails → memory → RAG → mode → engine → guardrails → save → respond.
    """
    if not req.message.strip() and not req.image_base64:
        raise HTTPException(400, "Provide a message, an image, or both.")

    if req.selected_mode and req.selected_mode not in VALID_MODES:
        raise HTTPException(422, f"Invalid mode. Must be one of: {sorted(VALID_MODES)}")

    orchestrator = TutorOrchestrator(db)
    result = await orchestrator.handle_message(
        student_id=student_id,
        session_id=req.session_id,
        message=req.message,
        selected_mode=req.selected_mode,
        image_base64=req.image_base64,
        conversation_history=req.conversation_history,
    )

    graphs_out = []
    for g in result.get("graphs", []):
        if isinstance(g, dict):
            # Build Desmos config if present
            desmos_data = None
            if g.get("desmos"):
                d = g["desmos"]
                desmos_data = DesmosConfig(
                    expressions=[DesmosExpression(**e) for e in d.get("expressions", [])],
                    bounds=DesmosBounds(**d["bounds"]) if d.get("bounds") else None,
                )

            graphs_out.append(GraphOutput(
                graph_type=g.get("graph_type"),
                image_base64=g.get("image_base64"),
                desmos=desmos_data,
            ))

    return MessageResponse(
        response=result["response"],
        subject=result.get("subject"),
        topic=result.get("topic"),
        mode=result.get("mode"),
        mode_source=result.get("mode_source"),
        tools_used=result.get("tools_used", []),
        graphs=graphs_out,
        validation_flags=result.get("validation_flags", []),
        suggestions=result.get("suggestions", []),
    )


@router.post("/close-session", response_model=CloseSessionResponse)
async def close_session(
    req: CloseSessionRequest,
    student_id: str = Depends(get_current_student_id),
    db: Session = Depends(get_db),
):
    """Close the session, generate summary, update student mastery."""
    memory = MemoryManager(db)
    session_data = await memory.close_and_update(student_id, req.session_id)

    return CloseSessionResponse(
        session_summary=session_data.get("session_summary"),
        total_problems=session_data.get("total_problems", 0),
        success_rate=session_data.get("success_rate", 0.0),
    )
