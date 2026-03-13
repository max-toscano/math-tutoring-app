"""
common_mistakes.py
Defines common student math mistake patterns.
The AI can use this to proactively watch for and address these patterns.
"""

COMMON_MATH_MISTAKES: list[str] = [
    "Forgetting to apply the order of operations (PEMDAS).",
    "Sign errors when distributing negatives.",
    "Confusing perimeter with area.",
    "Misapplying the quadratic formula.",
    "Skipping steps and making arithmetic errors mid-problem.",
]


def get_common_mistakes() -> list[str]:
    """Return the full list of common math mistakes."""
    return COMMON_MATH_MISTAKES
