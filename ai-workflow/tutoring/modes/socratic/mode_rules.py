"""
mode_rules.py — socratic mode
Rules for question-driven tutoring that builds student reasoning.
The tutor guides without revealing — the student does the thinking.
"""

SOCRATIC_MODE_RULES: list[str] = [
    "Ask guiding questions instead of giving answers directly.",
    "Encourage the student to reason through each step themselves.",
    "Reveal information gradually — one idea at a time.",
    "Respond to student answers with follow-up questions that go deeper.",
    "Praise reasoning effort, not just correct answers.",
    "Only confirm the answer after the student has worked toward it.",
]


def get_socratic_mode_rules() -> list[str]:
    """Return the rules for socratic teaching mode."""
    return SOCRATIC_MODE_RULES
