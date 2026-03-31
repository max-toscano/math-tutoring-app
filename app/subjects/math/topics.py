"""
subjects/math/topics.py
Math topic definitions and helper logic.

Used by the math engine to understand topic context.
The RAG layer handles topic detection — this file provides
supplementary topic metadata.
"""

MATH_TOPICS = {
    # Trigonometry
    "pythagorean_identity": {"display": "Pythagorean Identity", "chapter": "trig-identities", "subject": "trigonometry"},
    "double_angle": {"display": "Double Angle Formulas", "chapter": "trig-identities", "subject": "trigonometry"},
    "sum_to_product": {"display": "Sum-to-Product Formulas", "chapter": "trig-identities", "subject": "trigonometry"},
    "half_angle": {"display": "Half Angle Formulas", "chapter": "trig-identities", "subject": "trigonometry"},
    "unit_circle": {"display": "The Unit Circle", "chapter": "unit-circle", "subject": "trigonometry"},
    "six_trig_ratios": {"display": "Six Trig Ratios", "chapter": "right-triangle-trig", "subject": "trigonometry"},

    # Calculus — Derivatives
    "derivative_definition": {"display": "Definition of the Derivative", "chapter": "defining-the-derivative", "subject": "calculus"},
    "power_rule": {"display": "The Power Rule", "chapter": "differentiation-rules", "subject": "calculus"},
    "product_rule": {"display": "The Product Rule", "chapter": "differentiation-rules", "subject": "calculus"},
    "chain_rule": {"display": "The Chain Rule", "chapter": "chain-rule-and-advanced", "subject": "calculus"},

    # Calculus — Integration
    "antiderivatives": {"display": "Antiderivatives", "chapter": "intro-to-integration", "subject": "calculus"},
    "riemann_sums": {"display": "Riemann Sums", "chapter": "intro-to-integration", "subject": "calculus"},
    "fundamental_theorem": {"display": "Fundamental Theorem of Calculus", "chapter": "fundamental-theorem", "subject": "calculus"},
    "u_substitution": {"display": "U-Substitution", "chapter": "integration-techniques", "subject": "calculus"},
    "integration_by_parts": {"display": "Integration by Parts", "chapter": "integration-techniques", "subject": "calculus"},

    # Algebra
    "quadratic_formula": {"display": "Quadratic Formula", "chapter": "quadratic-equations", "subject": "algebra"},
    "factoring": {"display": "Factoring", "chapter": "polynomials", "subject": "algebra"},
}


def get_topic_info(topic_slug: str) -> dict | None:
    """Get metadata for a topic by its slug."""
    return MATH_TOPICS.get(topic_slug)


def get_display_name(topic_slug: str) -> str:
    """Get the human-readable name for a topic."""
    info = MATH_TOPICS.get(topic_slug)
    return info["display"] if info else topic_slug.replace("_", " ").title()
