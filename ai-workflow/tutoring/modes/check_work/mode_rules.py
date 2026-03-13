"""
mode_rules.py — check_work mode
Rules for reviewing student-submitted work and explaining errors.
The tutor acts as a reviewer — finding, explaining, and correcting mistakes.
"""

CHECK_WORK_MODE_RULES: list[str] = [
    "Carefully inspect the student's submitted work before responding.",
    "Identify the exact step where the error occurred.",
    "Explain clearly why the step is wrong — not just that it is wrong.",
    "Show the correct approach for that step without redoing the whole problem.",
    "If the work is correct, confirm it with a clear and specific explanation of why.",
    "Be encouraging — mistakes are part of learning.",
]


def get_check_work_mode_rules() -> list[str]:
    """Return the rules for check_work teaching mode."""
    return CHECK_WORK_MODE_RULES
