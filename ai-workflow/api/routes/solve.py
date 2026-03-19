"""
solve.py
Endpoint for solving math problems from scanned images or typed text.
Returns a structured, step-by-step breakdown with the answer.
"""

import json
import os
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from openai import OpenAI

from db.database import get_db
from db.models import Interaction
from api.schemas import SolveImageRequest, SolveTextRequest, SolveResponse, SolveStep
from api.auth_middleware import get_current_user_id
from prompts.math_solver_prompt import MATH_SOLVER_PROMPT, MATH_SOLVER_TEXT_PROMPT

router = APIRouter(prefix="/solve", tags=["solve"])

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def _solve_with_image(image_base64: str, mime_type: str, student_question: str | None) -> dict:
    """Send an image to the LLM and get a structured math solution."""
    user_content: list[dict] = [
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:{mime_type};base64,{image_base64}",
                "detail": "high",
            },
        },
        {
            "type": "text",
            "text": (
                f"Solve the math problem in this image. Student's question: {student_question}"
                if student_question
                else "Analyze and solve the math problem in this image. Show every step."
            ),
        },
    ]

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        messages=[
            {"role": "system", "content": MATH_SOLVER_PROMPT},
            {"role": "user", "content": user_content},
        ],
        temperature=0.1,
        max_tokens=4000,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    return json.loads(raw)


def _solve_with_text(problem_text: str, student_question: str | None) -> dict:
    """Send a text problem to the LLM and get a structured math solution."""
    user_msg = problem_text
    if student_question:
        user_msg = f"Problem: {problem_text}\n\nStudent's question: {student_question}"

    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        messages=[
            {"role": "system", "content": MATH_SOLVER_TEXT_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.1,
        max_tokens=4000,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    return json.loads(raw)


def _parse_solve_response(data: dict) -> SolveResponse:
    """Parse the raw LLM JSON into a validated SolveResponse."""
    steps = [
        SolveStep(
            step=s.get("step", i + 1),
            title=s.get("title", ""),
            math=s.get("math"),
            explanation=s.get("explanation", ""),
            note=s.get("note"),
        )
        for i, s in enumerate(data.get("steps", []))
    ]

    return SolveResponse(
        problem=data.get("problem", ""),
        topic=data.get("topic", ""),
        subject_area=data.get("subject_area", ""),
        difficulty=data.get("difficulty", "Medium"),
        answer=data.get("answer", ""),
        method=data.get("method", ""),
        steps=steps,
        verification=data.get("verification"),
        concepts=data.get("concepts", []),
        prerequisites=data.get("prerequisites", []),
        common_mistakes=data.get("common_mistakes", []),
        tip=data.get("tip"),
    )


@router.post("/image", response_model=SolveResponse)
def solve_image(
    req: SolveImageRequest,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Solve a math problem from a scanned image. Returns structured step-by-step breakdown."""
    if not req.image_base64:
        raise HTTPException(400, "image_base64 is required")

    data = _solve_with_image(req.image_base64, req.mime_type, req.student_question)
    result = _parse_solve_response(data)

    # Store interaction for analytics
    interaction = Interaction(
        user_id=user_id,
        subject="math",
        topic=result.topic,
        mode="solve",
        student_input=f"[image scan] {result.problem}",
        ai_response=result.answer,
        is_correct=None,
        difficulty=result.difficulty,
        concepts=result.concepts,
    )
    db.add(interaction)
    db.commit()

    return result


@router.post("/text", response_model=SolveResponse)
def solve_text(
    req: SolveTextRequest,
    user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Solve a math problem from typed text. Returns structured step-by-step breakdown."""
    if not req.problem_text.strip():
        raise HTTPException(400, "problem_text is required")

    data = _solve_with_text(req.problem_text, req.student_question)
    result = _parse_solve_response(data)

    # Store interaction for analytics
    interaction = Interaction(
        user_id=user_id,
        subject="math",
        topic=result.topic,
        mode="solve",
        student_input=req.problem_text,
        ai_response=result.answer,
        is_correct=None,
        difficulty=result.difficulty,
        concepts=result.concepts,
    )
    db.add(interaction)
    db.commit()

    return result
