"""
rag/retrieval/topic_retriever.py
Detect what math topic a student is asking about.

Pure keyword matching — no database, no embeddings, no LLM call.
Just fast pattern matching against known math topics.
"""

import logging

logger = logging.getLogger(__name__)

# Topic → keywords that indicate this topic
TOPIC_KEYWORDS: dict[str, list[str]] = {
    # Trigonometry
    "pythagorean_identity": ["pythagorean", "sin squared", "cos squared", "sin^2", "cos^2", "sin²", "cos²"],
    "double_angle": ["double angle", "sin(2", "cos(2", "sin 2", "cos 2", "double-angle", "2theta", "2θ"],
    "sum_to_product": ["sum to product", "product to sum", "sum-to-product"],
    "unit_circle": ["unit circle", "reference angle", "quadrant", "special angle"],
    "trig_identities": ["trig identity", "trig identities", "verify identity", "prove identity"],
    "law_of_sines": ["law of sines", "sine rule"],
    "law_of_cosines": ["law of cosines", "cosine rule"],
    "inverse_trig": ["arcsin", "arccos", "arctan", "inverse trig", "sin^-1", "cos^-1"],
    "graphing_trig": ["graph sin", "graph cos", "amplitude", "period", "phase shift"],

    # Calculus — Limits & Continuity
    "limits_intro": ["limit", "lim ", "approaches", "limit of", "lim("],
    "continuity": ["continuous", "continuity", "discontinuity", "removable"],
    "squeeze_theorem": ["squeeze theorem", "sandwich theorem"],

    # Calculus — Derivatives
    "derivative_definition": ["definition of derivative", "difference quotient", "limit definition"],
    "power_rule": ["power rule", "derivative of x^", "nxⁿ", "nx^"],
    "product_quotient_rule": ["product rule", "quotient rule", "(fg)'"],
    "chain_rule": ["chain rule", "composite", "f(g(x))", "dy/du", "inner function", "outer function"],
    "implicit_differentiation": ["implicit", "implicitly", "dy/dx in terms of"],
    "related_rates": ["related rates", "rate of change", "changing rate"],
    "optimization": ["optimize", "optimization", "maximum", "minimum", "max/min"],
    "lhopitals_rule": ["l'hopital", "lhopital", "0/0", "indeterminate"],

    # Calculus — Integration
    "antiderivatives": ["antiderivative", "indefinite integral", "∫", "integral of", "integrate"],
    "fundamental_theorem": ["fundamental theorem", "ftc", "F(b) - F(a)", "definite integral"],
    "u_substitution": ["u-sub", "u substitution", "u-substitution", "substitution method"],
    "integration_by_parts": ["integration by parts", "ibp", "∫u dv", "uv - ∫v du"],
    "riemann_sums": ["riemann sum", "left sum", "right sum", "midpoint sum"],

    # Calculus 2
    "improper_integrals": ["improper integral", "diverge", "converge integral"],
    "sequences_series": ["sequence", "series", "convergence", "divergence", "sum of"],
    "taylor_series": ["taylor", "maclaurin", "power series", "taylor series"],
    "partial_fractions": ["partial fraction", "partial fractions"],

    # Calculus 3
    "partial_derivatives": ["partial derivative", "∂", "multivariable"],
    "multiple_integrals": ["double integral", "triple integral", "iterated integral"],
    "vectors": ["vector", "dot product", "cross product", "magnitude"],
    "gradient": ["gradient", "∇", "directional derivative"],

    # Differential Equations
    "separable_ode": ["separable", "separate variables", "dy/dx ="],
    "linear_ode": ["linear ode", "first order linear", "integrating factor"],
    "second_order_ode": ["second order", "y'' +", "characteristic equation"],
    "laplace_transform": ["laplace", "laplace transform", "inverse laplace"],

    # Linear Algebra
    "matrix_operations": ["matrix", "matrices", "matrix multiply", "transpose"],
    "determinant": ["determinant", "det(", "det A"],
    "eigenvalues": ["eigenvalue", "eigenvector", "characteristic polynomial"],
    "row_reduction": ["row reduce", "rref", "gaussian elimination", "row echelon"],
    "linear_systems": ["system of equations", "Ax = b", "linear system"],
    "vector_spaces": ["vector space", "subspace", "basis", "dimension", "span"],

    # Algebra
    "quadratic_formula": ["quadratic", "ax² + bx", "discriminant", "b² - 4ac", "quadratic formula"],
    "difference_of_squares": ["difference of squares", "a² - b²", "x² -"],
    "factoring": ["factor", "factoring", "factored form"],
    "completing_the_square": ["completing the square", "complete the square"],
    "logarithms": ["logarithm", "log(", "ln(", "log base", "natural log"],
    "exponents": ["exponent", "exponential", "e^x", "growth", "decay"],
}

# Topic → subject mapping (no database needed)
TOPIC_SUBJECTS: dict[str, str] = {
    # Trig
    "pythagorean_identity": "trigonometry", "double_angle": "trigonometry",
    "sum_to_product": "trigonometry", "unit_circle": "trigonometry",
    "trig_identities": "trigonometry", "law_of_sines": "trigonometry",
    "law_of_cosines": "trigonometry", "inverse_trig": "trigonometry",
    "graphing_trig": "trigonometry",
    # Calc 1
    "limits_intro": "calculus", "continuity": "calculus", "squeeze_theorem": "calculus",
    "derivative_definition": "calculus", "power_rule": "calculus",
    "product_quotient_rule": "calculus", "chain_rule": "calculus",
    "implicit_differentiation": "calculus", "related_rates": "calculus",
    "optimization": "calculus", "lhopitals_rule": "calculus",
    "antiderivatives": "calculus", "fundamental_theorem": "calculus",
    "u_substitution": "calculus", "integration_by_parts": "calculus",
    "riemann_sums": "calculus",
    # Calc 2
    "improper_integrals": "calculus_2", "sequences_series": "calculus_2",
    "taylor_series": "calculus_2", "partial_fractions": "calculus_2",
    # Calc 3
    "partial_derivatives": "calculus_3", "multiple_integrals": "calculus_3",
    "vectors": "calculus_3", "gradient": "calculus_3",
    # Diff Eq
    "separable_ode": "differential_equations", "linear_ode": "differential_equations",
    "second_order_ode": "differential_equations", "laplace_transform": "differential_equations",
    # Linear Algebra
    "matrix_operations": "linear_algebra", "determinant": "linear_algebra",
    "eigenvalues": "linear_algebra", "row_reduction": "linear_algebra",
    "linear_systems": "linear_algebra", "vector_spaces": "linear_algebra",
    # Algebra
    "quadratic_formula": "algebra", "difference_of_squares": "algebra",
    "factoring": "algebra", "completing_the_square": "algebra",
    "logarithms": "algebra", "exponents": "algebra",
}


class TopicRetriever:
    """Detect the math topic from a student's question. No database needed."""

    def __init__(self, db=None):
        # db parameter kept for compatibility but not used
        pass

    def detect_topic(self, query: str) -> dict:
        """
        Detect the topic from keyword matching.
        No database, no embeddings, no LLM call.
        """
        query_lower = query.lower()

        best_match = None
        best_score = 0

        for topic_slug, keywords in TOPIC_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in query_lower)
            if score > best_score:
                best_score = score
                best_match = topic_slug

        if best_match and best_score > 0:
            return {
                "topic": best_match,
                "subject": TOPIC_SUBJECTS.get(best_match, "math"),
                "confidence": min(best_score / 2, 1.0),
            }

        return {
            "topic": "unknown",
            "subject": "math",
            "confidence": 0.0,
        }
