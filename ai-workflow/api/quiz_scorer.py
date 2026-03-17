"""
quiz_scorer.py
Tracks quiz state across the 5-question quiz flow and persists results.

Used by the /learn/lesson endpoint to:
1. Track answers as they come in (quiz_result from AI response)
2. After question 5: validate score, insert quiz_attempt, update progress
3. Save individual quiz interactions to the interactions table

The quiz state is reconstructed from conversation history each request —
no server-side session state needed.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from db.models import QuizAttempt, UserTopicProgress, Interaction
from api.phase_machine import resolve_quiz_outcome, get_status_for_phase


def extract_quiz_state(conversation_history: list[dict]) -> dict:
    """Reconstruct quiz state from the conversation's AI responses.

    Scans all assistant messages for quiz_result objects to rebuild
    the running tally. This makes the endpoint stateless.

    Args:
        conversation_history: List of {"role": ..., "content": ...} dicts.
            Assistant content may be JSON strings containing quiz_result.

    Returns:
        {
            "question_number": int,   # how many quiz questions answered so far
            "correct_count": int,
            "answers": [              # one per answered question
                {
                    "question_number": int,
                    "is_correct": bool,
                    "concept_tested": str,
                    "explanation": str,
                }
            ]
        }
    """
    import json

    state = {"question_number": 0, "correct_count": 0, "answers": []}

    for msg in (conversation_history or []):
        if msg.get("role") != "assistant":
            continue
        content = msg.get("content", "")
        try:
            parsed = json.loads(content) if isinstance(content, str) else content
        except (json.JSONDecodeError, TypeError):
            continue

        qr = parsed.get("quiz_result") if isinstance(parsed, dict) else None
        if not qr:
            continue

        state["question_number"] += 1
        if qr.get("is_correct"):
            state["correct_count"] += 1
        state["answers"].append({
            "question_number": state["question_number"],
            "is_correct": bool(qr.get("is_correct")),
            "concept_tested": qr.get("concept_tested", ""),
            "explanation": qr.get("explanation", ""),
        })

    return state


def process_quiz_result(
    ai_response: dict,
    quiz_state: dict,
) -> dict:
    """Process a quiz_result from the current AI response and update quiz state.

    Call this AFTER the AI responds, before saving. Updates the state dict
    in-place and returns it.

    Args:
        ai_response: Parsed JSON from the AI's response.
        quiz_state: Current state from extract_quiz_state().

    Returns:
        Updated quiz_state dict.
    """
    qr = ai_response.get("quiz_result")
    if not qr:
        return quiz_state

    quiz_state["question_number"] += 1
    if qr.get("is_correct"):
        quiz_state["correct_count"] += 1
    quiz_state["answers"].append({
        "question_number": quiz_state["question_number"],
        "is_correct": bool(qr.get("is_correct")),
        "concept_tested": qr.get("concept_tested", ""),
        "explanation": qr.get("explanation", ""),
    })

    return quiz_state


def is_quiz_complete(quiz_state: dict) -> bool:
    """Check if all 5 quiz questions have been answered."""
    return quiz_state["question_number"] >= 5


def finalize_quiz(
    db: Session,
    user_id,
    progress: UserTopicProgress,
    quiz_state: dict,
    quiz_summary: dict | None,
) -> dict:
    """After all 5 questions: save quiz attempt, update progress, return outcome.

    Uses the app's own correct_count (not the AI's quiz_summary.passed)
    to determine pass/fail.

    Args:
        db: SQLAlchemy session.
        user_id: The user's UUID.
        progress: The UserTopicProgress row for this topic.
        quiz_state: Final quiz state with all 5 answers.
        quiz_summary: The AI's quiz_summary dict (used for missed_concepts only).

    Returns:
        {
            "score": int,
            "passed": bool,
            "new_phase": str,       # "done" or "review"
            "new_status": str,      # "completed" or "failed_last_attempt"
            "missed_concepts": list[str],
        }
    """
    score = quiz_state["correct_count"]
    new_phase = resolve_quiz_outcome(score)
    passed = new_phase == "done"
    new_status = get_status_for_phase(new_phase, quiz_passed=passed)

    # Build missed_concepts from our own tracking (don't trust AI's list blindly)
    missed_concepts = [
        a["concept_tested"]
        for a in quiz_state["answers"]
        if not a["is_correct"] and a["concept_tested"]
    ]

    # Build questions JSONB for the quiz_attempts row
    questions_json = []
    for a in quiz_state["answers"]:
        questions_json.append({
            "question_number": a["question_number"],
            "is_correct": a["is_correct"],
            "concept_tested": a["concept_tested"],
            "explanation": a["explanation"],
        })

    # Insert quiz_attempts row
    attempt_number = (progress.quiz_attempts or 0) + 1
    quiz_attempt = QuizAttempt(
        user_id=user_id,
        progress_id=progress.id,
        subject=progress.subject,
        chapter=progress.chapter,
        topic=progress.topic,
        attempt_number=attempt_number,
        score=score,
        passed=passed,
        questions=questions_json,
        missed_concepts=missed_concepts,
    )
    db.add(quiz_attempt)

    # Update progress row
    progress.phase = new_phase
    progress.status = new_status
    progress.quiz_attempts = attempt_number
    if progress.best_quiz_score is None or score > progress.best_quiz_score:
        progress.best_quiz_score = score
    progress.updated_at = datetime.now(timezone.utc)

    db.flush()  # let the caller commit

    return {
        "score": score,
        "passed": passed,
        "new_phase": new_phase,
        "new_status": new_status,
        "missed_concepts": missed_concepts,
    }


def save_quiz_interaction(
    db: Session,
    user_id,
    subject: str,
    topic: str,
    student_input: str,
    ai_response_text: str,
    quiz_result: dict | None,
):
    """Save a single quiz Q&A exchange to the interactions table.

    Args:
        db: SQLAlchemy session.
        user_id: The user's UUID.
        subject: Subject slug.
        topic: Topic slug.
        student_input: What the student said.
        ai_response_text: The AI's message text.
        quiz_result: The quiz_result dict from the AI response, if any.
    """
    interaction = Interaction(
        user_id=user_id,
        subject=subject,
        topic=topic,
        mode="quiz",
        student_input=student_input,
        ai_response=ai_response_text,
        is_correct=quiz_result.get("is_correct") if quiz_result else None,
        concepts=[quiz_result.get("concept_tested")] if quiz_result and quiz_result.get("concept_tested") else [],
    )
    db.add(interaction)
