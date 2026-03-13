"""
__init__.py
Math subject module entry point.
Exports the key functions and constants for use by the rest of the ai-workflow layer.
"""

from .subject_rules import MATH_SUBJECT_RULES, get_rules
from .topic_router import route_math_topic
from .teaching_strategies import (
    solve_step_by_step,
    explain_concept,
    check_answer,
    generate_hint,
)
from .common_mistakes import COMMON_MATH_MISTAKES, get_common_mistakes
from .response_patterns import (
    openers,
    guided_questions,
    step_transitions,
    mistake_corrections,
    learning_checkpoints,
    closers,
)
from .evaluator import evaluate_math_response, EvaluationResult

__all__ = [
    # Rules
    "MATH_SUBJECT_RULES",
    "get_rules",
    # Topic routing
    "route_math_topic",
    # Teaching strategies
    "solve_step_by_step",
    "explain_concept",
    "check_answer",
    "generate_hint",
    # Common mistakes
    "COMMON_MATH_MISTAKES",
    "get_common_mistakes",
    # Response patterns
    "openers",
    "guided_questions",
    "step_transitions",
    "mistake_corrections",
    "learning_checkpoints",
    "closers",
    # Evaluator
    "evaluate_math_response",
    "EvaluationResult",
]
