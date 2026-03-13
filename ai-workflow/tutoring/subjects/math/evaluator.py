"""
evaluator.py
Evaluates a student's tutoring response and returns a structured result.
This will later plug into the broader session evaluation system.
"""

from typing import TypedDict


class EvaluationResult(TypedDict):
    passed: bool
    score: int        # 0–100
    issues: list[str] # List of identified problems, if any


def evaluate_math_response(response: str) -> EvaluationResult:
    """
    Evaluate the quality of a math tutoring response.
    Returns a dict with passed, score, and issues.
    TODO: Replace placeholder logic with real evaluation rules.
    """
    # Placeholder — always returns a neutral passing result.
    return EvaluationResult(
        passed=True,
        score=100,
        issues=[],
    )
