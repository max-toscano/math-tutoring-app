"""
tutor.py
The main tutoring endpoint. Calls the LLM, parses structured response,
stores the interaction in the DB, and returns the result.
"""

import json
import os
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from openai import OpenAI

from db.database import get_db
from db.models import Interaction
from api.schemas import TutorRequest, TutorResponse, Assessment, VALID_SUBJECTS, VALID_MODES
from api.auth_middleware import get_current_user_id
from prompts.system_prompt import build_system_prompt

router = APIRouter(prefix="/tutor", tags=["tutor"])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _call_llm(system_prompt: str, student_input: str, image_base64: str | None = None) -> dict:
    """Send the prompt to the LLM and parse the JSON response."""
    messages = [{"role": "system", "content": system_prompt}]

    if image_base64:
        messages.append({
            "role": "user",
            "content": [
                {"type": "text", "text": student_input},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}},
            ],
        })
    else:
        messages.append({"role": "user", "content": student_input})

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        messages=messages,
        temperature=0.3,
        max_tokens=2500,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    return json.loads(raw)


@router.post("/respond", response_model=TutorResponse)
def tutor_respond(
    req: TutorRequest,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Accept student input, get AI tutoring response, store interaction."""
    subject = req.subject.lower().strip()
    mode = req.mode.lower().strip()

    if subject not in VALID_SUBJECTS:
        raise HTTPException(400, f"Invalid subject. Choose from: {VALID_SUBJECTS}")
    if mode not in VALID_MODES:
        raise HTTPException(400, f"Invalid mode. Choose from: {VALID_MODES}")

    # Build prompt and call LLM
    system_prompt = build_system_prompt(subject, mode)
    llm_result = _call_llm(system_prompt, req.student_input, req.image_base64)

    # Parse response
    response_text = llm_result.get("response_text", "")
    assessment_data = llm_result.get("assessment", {})

    assessment = Assessment(
        is_correct=assessment_data.get("is_correct"),
        mistake_type=assessment_data.get("mistake_type"),
        topic=assessment_data.get("topic"),
        difficulty=assessment_data.get("difficulty"),
        concepts=assessment_data.get("concepts", []),
    )

    # Store interaction in DB
    interaction = Interaction(
        user_id=user_id,
        subject=subject,
        topic=assessment.topic,
        mode=mode,
        student_input=req.student_input,
        ai_response=response_text,
        is_correct=assessment.is_correct,
        mistake_type=assessment.mistake_type,
        difficulty=assessment.difficulty,
        concepts=assessment.concepts,
    )
    db.add(interaction)
    db.commit()

    return TutorResponse(
        subject=subject,
        mode=mode,
        response_text=response_text,
        assessment=assessment,
    )
