"""
teaching_strategies.py
Defines the different approaches the AI can take when helping a student.
Each strategy will later map to a specific prompt style or workflow.
"""


def solve_step_by_step(problem: str) -> str:
    """
    Walk the student through a problem one step at a time.
    TODO: Replace with real prompt-building logic.
    """
    return f"[step-by-step placeholder for: '{problem}']"


def explain_concept(concept: str) -> str:
    """
    Explain the underlying concept before solving.
    TODO: Replace with real concept explanation prompt.
    """
    return f"[explain concept placeholder for: '{concept}']"


def check_answer(student_answer: str, correct_answer: str) -> str:
    """
    Verify whether the student's answer is correct and provide feedback.
    TODO: Replace with real answer-check prompt with feedback.
    """
    return f"[check answer placeholder — student: '{student_answer}', correct: '{correct_answer}']"


def generate_hint(problem: str, hint_level: int = 1) -> str:
    """
    Generate a progressive hint for the student without revealing the full answer.
    hint_level controls how much guidance is given (1 = subtle, 3 = strong).
    TODO: Replace with real hint-generation logic tied to topic and difficulty.
    """
    return f"[hint level {hint_level} placeholder for: '{problem}']"
