"""
subject_rules.py
Defines the core teaching rules the AI must follow when tutoring math.
These rules shape how the AI explains, guides, and responds to students.
"""

MATH_SUBJECT_RULES: list[str] = [
    "Always explain each step clearly before moving to the next.",
    "Never skip reasoning — show why, not just how.",
    "Guide the student toward the answer before revealing it.",
    "Use simple language; avoid unnecessary jargon.",
    "Check for understanding before moving forward.",
]


def get_rules() -> list[str]:
    """Return the full list of math teaching rules."""
    return MATH_SUBJECT_RULES
