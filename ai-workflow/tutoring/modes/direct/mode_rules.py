"""
mode_rules.py — direct mode
Rules for clear, instructional, step-by-step tutoring.
The tutor explains directly without withholding information.
"""

DIRECT_MODE_RULES: list[str] = [
    "Explain the concept clearly and completely.",
    "Provide explicit steps when walking through a solution.",
    "Do not withhold information — the student needs clarity, not puzzles.",
    "Use simple, accessible language at all times.",
    "Be warm and supportive in tone.",
    "Confirm understanding before moving to the next step.",
]


def get_direct_mode_rules() -> list[str]:
    """Return the rules for direct teaching mode."""
    return DIRECT_MODE_RULES
