"""
phase_machine.py
State machine for the 5-phase teaching flow.

Controls phase transitions so students follow the structured path:
  lesson → practice → quiz → review (if failed) → quiz → done

The APP enforces transitions, not the AI. The AI can suggest a phase_transition
in its JSON response, but this module validates it before applying.

Phase values: None | "lesson" | "practice" | "quiz" | "review" | "done"
"""

# ─── Valid Transitions ──────────────────────────────────────────────────────
# Maps current phase → set of phases the AI is allowed to request.
# Quiz outcomes (done/review) are handled separately by resolve_quiz_outcome().

VALID_TRANSITIONS: dict[str | None, set[str]] = {
    None:        {"lesson"},
    "lesson":    {"practice", "quiz"},
    "practice":  {"quiz"},
    "quiz":      set(),       # quiz outcome is decided by the app, not the AI
    "review":    {"quiz"},
    "done":      set(),       # done is terminal — revisits don't change phase
}

QUIZ_PASS_THRESHOLD = 3  # out of 5


# ─── Public API ─────────────────────────────────────────────────────────────

def get_initial_phase() -> str:
    """Return the phase for a student opening a topic for the first time."""
    return "lesson"


def validate_transition(current_phase: str | None, requested_phase: str) -> str | None:
    """Check if a phase transition requested by the AI is allowed.

    Args:
        current_phase:    The student's current phase (from user_topic_progress.phase)
        requested_phase:  The phase_transition value from the AI's JSON response

    Returns:
        The new phase if the transition is valid, or None if rejected.
    """
    allowed = VALID_TRANSITIONS.get(current_phase, set())
    if requested_phase in allowed:
        return requested_phase
    return None


def resolve_quiz_outcome(score: int) -> str:
    """Determine the next phase after a completed quiz (all 5 questions answered).

    The app calls this — the AI never decides pass/fail.

    Args:
        score: Number of correct answers out of 5

    Returns:
        "done" if score >= 3, "review" if score < 3
    """
    if score >= QUIZ_PASS_THRESHOLD:
        return "done"
    return "review"


def get_status_for_phase(phase: str, quiz_passed: bool = False) -> str:
    """Return the appropriate user_topic_progress.status for a given phase.

    Args:
        phase:        The new phase being transitioned to
        quiz_passed:  Whether the student just passed the quiz

    Returns:
        Status string: "not_started", "in_progress", "completed", or "failed_last_attempt"
    """
    if phase == "done" and quiz_passed:
        return "completed"
    if phase == "review":
        return "failed_last_attempt"
    if phase in ("lesson", "practice", "quiz"):
        return "in_progress"
    if phase == "done":
        return "completed"
    return "in_progress"


def can_skip_to_quiz(current_phase: str | None) -> bool:
    """Check if the student is allowed to skip directly to the quiz.

    Students can skip from lesson (bypass practice) but not from other phases.
    """
    return current_phase in (None, "lesson")
