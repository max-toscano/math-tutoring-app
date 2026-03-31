"""
guardrails/policy.py
Defines tutoring rules and safety constraints.
Single source of truth for all policy constants.
"""

ALLOWED_SUBJECTS = ["math"]

VALID_MODES = {"auto", "explain", "guide_me", "hint", "check_answer"}

MAX_RESPONSE_WORDS = 200
MAX_MESSAGE_LENGTH = 5000
MAX_ITERATIONS = 8
MAX_SUB_CALLS = 3

# Content patterns that should never appear in responses
BLOCKED_CONTENT_PATTERNS: list[str] = []

# Mode-specific compliance rules
MODE_RULES = {
    "auto": {
        "must_end_with_question": False,
        "description": "Adapt to the student's situation automatically.",
    },
    "explain": {
        "must_end_with_question": False,
        "description": "Explain the concept behind the problem with examples.",
    },
    "guide_me": {
        "must_end_with_question": False,
        "description": "Walk the student through step by step.",
    },
    "hint": {
        "must_end_with_question": False,
        "description": "Give a small nudge without revealing the solution.",
    },
    "check_answer": {
        "must_end_with_question": False,
        "description": "Verify the student's work and point out errors specifically.",
    },
}
