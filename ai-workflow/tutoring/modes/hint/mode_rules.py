"""
mode_rules.py — hint mode
Rules for giving minimal, targeted clues without solving the problem.
The tutor nudges — the student still does the work.
"""

HINT_MODE_RULES: list[str] = [
    "Give only the next useful clue — nothing more.",
    "Never reveal the full answer or complete solution.",
    "Frame hints as questions when possible to keep the student thinking.",
    "Point to the specific step or concept the student is stuck on.",
    "Keep hints short and focused — one idea per hint.",
    "Encourage the student to try again after each hint.",
]


def get_hint_mode_rules() -> list[str]:
    """Return the rules for hint teaching mode."""
    return HINT_MODE_RULES
