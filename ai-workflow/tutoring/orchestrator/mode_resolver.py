"""
mode_resolver.py
Determines which teaching mode should be used for the student's request.

Responsibility:
    If the caller specifies a mode, use it directly.
    Otherwise, inspect the student's input for intent signals
    and return the best matching mode. Defaults to "direct".

Supported modes:
    direct      — explain clearly and provide steps
    socratic    — guide with questions, encourage reasoning
    hint        — give only the next useful clue
    check_work  — inspect the student's answer and identify errors
"""

# Keyword map: mode -> trigger phrases/words
_MODE_KEYWORDS: dict[str, list[str]] = {
    "hint": [
        "hint", "clue", "nudge", "point me", "give me a hint",
        "just a hint", "help me start",
    ],
    "check_work": [
        "check my work", "is this right", "is this correct",
        "did i get it", "review my answer", "look at my answer",
        "am i right", "is my answer",
    ],
    "socratic": [
        "help me understand", "guide me", "walk me through",
        "help me think", "why does", "how does this work",
        "can you explain why",
    ],
}


def resolve_mode(
    student_input: str,
    requested_mode: str | None = None,
) -> str:
    """
    Resolve the teaching mode for a tutoring request.

    Args:
        student_input:    The raw text from the student.
        requested_mode:   Optional explicit mode from the API request.

    Returns:
        A mode string: "direct", "socratic", "hint", or "check_work".
        Defaults to "direct" when no signal is found.
    """
    # Caller explicitly specified a mode — trust it.
    if requested_mode:
        return requested_mode.lower().strip()

    # Keyword-based detection — check in priority order.
    lowered = student_input.lower()
    for mode, keywords in _MODE_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return mode

    # TODO: Replace keyword matching with an LLM-based intent classifier.
    return "direct"
