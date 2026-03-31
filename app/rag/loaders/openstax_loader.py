"""
rag/loaders/openstax_loader.py
Load OpenStax math textbook content for RAG.

Loads content from local files if available, otherwise provides
hardcoded sample content for development/testing.
"""

import os
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class OpenStaxLoader:
    """Load OpenStax textbook content into structured documents."""

    def __init__(self, data_path: str):
        self.data_path = Path(data_path)

    def load(self) -> list[dict]:
        """
        Load OpenStax content from the data directory.

        Each document has:
          - content: the text
          - metadata: {source, chapter, section, topic, subject}

        Falls back to sample content if no files exist yet.
        """
        if self.data_path.exists():
            documents = self._load_from_files()
            if documents:
                logger.info(f"Loaded {len(documents)} documents from {self.data_path}")
                return documents

        logger.info("No OpenStax files found — using sample content")
        return self._sample_content()

    def _load_from_files(self) -> list[dict]:
        """Load documents from JSON files in the data directory."""
        documents = []
        for file_path in self.data_path.glob("**/*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if isinstance(data, list):
                    documents.extend(data)
                elif isinstance(data, dict) and "content" in data:
                    documents.append(data)
            except Exception as e:
                logger.warning(f"Failed to load {file_path}: {e}")
        return documents

    def _sample_content(self) -> list[dict]:
        """Return hardcoded OpenStax-style sample content for development."""
        return [
            {
                "content": (
                    "The Pythagorean identity states that for any angle θ, sin²θ + cos²θ = 1. "
                    "This identity is derived directly from the unit circle definition of sine and cosine. "
                    "If a point on the unit circle has coordinates (cos θ, sin θ), then by the Pythagorean theorem "
                    "applied to the right triangle formed with the origin, cos²θ + sin²θ = 1. "
                    "Two additional forms can be derived by dividing through by cos²θ or sin²θ: "
                    "tan²θ + 1 = sec²θ and 1 + cot²θ = csc²θ."
                ),
                "metadata": {"source": "openstax_algebra_trig", "chapter": "7", "section": "7.1", "topic": "pythagorean_identity", "subject": "trigonometry"},
            },
            {
                "content": (
                    "The double-angle formulas express trigonometric functions of 2θ in terms of θ. "
                    "The three primary double-angle identities are: sin(2θ) = 2sin(θ)cos(θ), "
                    "cos(2θ) = cos²(θ) − sin²(θ), and tan(2θ) = 2tan(θ)/(1 − tan²(θ)). "
                    "The cosine double-angle formula has two equivalent forms: cos(2θ) = 2cos²(θ) − 1 "
                    "and cos(2θ) = 1 − 2sin²(θ). These follow from substituting the Pythagorean identity."
                ),
                "metadata": {"source": "openstax_algebra_trig", "chapter": "7", "section": "7.3", "topic": "double_angle", "subject": "trigonometry"},
            },
            {
                "content": (
                    "The sum-to-product formulas allow us to rewrite sums or differences of sines and cosines "
                    "as products. The four formulas are: sin A + sin B = 2 sin((A+B)/2) cos((A−B)/2), "
                    "sin A − sin B = 2 cos((A+B)/2) sin((A−B)/2), cos A + cos B = 2 cos((A+B)/2) cos((A−B)/2), "
                    "and cos A − cos B = −2 sin((A+B)/2) sin((A−B)/2). These are derived by adding or subtracting "
                    "the sum and difference identities for sine and cosine."
                ),
                "metadata": {"source": "openstax_algebra_trig", "chapter": "7", "section": "7.4", "topic": "sum_to_product", "subject": "trigonometry"},
            },
            {
                "content": (
                    "The quadratic formula solves any equation of the form ax² + bx + c = 0. "
                    "The solutions are x = (−b ± √(b² − 4ac)) / (2a). The expression under the radical, "
                    "b² − 4ac, is called the discriminant. When the discriminant is positive, there are two "
                    "real solutions. When it equals zero, there is one repeated real solution. When it is negative, "
                    "the solutions are complex conjugates."
                ),
                "metadata": {"source": "openstax_algebra", "chapter": "2", "section": "2.5", "topic": "quadratic_formula", "subject": "algebra"},
            },
            {
                "content": (
                    "The derivative of a function f at a point x is defined as the limit "
                    "f'(x) = lim(h→0) [f(x+h) − f(x)] / h, provided this limit exists. "
                    "Geometrically, the derivative gives the slope of the tangent line to the curve y = f(x) "
                    "at the point (x, f(x)). A function is differentiable at a point if this limit exists, "
                    "and differentiability implies continuity but not vice versa."
                ),
                "metadata": {"source": "openstax_calculus", "chapter": "3", "section": "3.1", "topic": "derivative_definition", "subject": "calculus"},
            },
            {
                "content": (
                    "The power rule states that if f(x) = xⁿ where n is any real number, then f'(x) = nxⁿ⁻¹. "
                    "This rule, combined with the constant multiple rule and the sum rule, allows differentiation "
                    "of any polynomial. For example, if f(x) = 3x⁴ − 2x² + 5x − 1, then "
                    "f'(x) = 12x³ − 4x + 5."
                ),
                "metadata": {"source": "openstax_calculus", "chapter": "3", "section": "3.3", "topic": "power_rule", "subject": "calculus"},
            },
            {
                "content": (
                    "The chain rule is used to differentiate composite functions. If y = f(g(x)), then "
                    "dy/dx = f'(g(x)) · g'(x). In Leibniz notation, if y = f(u) and u = g(x), then "
                    "dy/dx = (dy/du)(du/dx). The chain rule is essential for differentiating functions "
                    "like sin(x²), e^(3x), or ln(cos x)."
                ),
                "metadata": {"source": "openstax_calculus", "chapter": "3", "section": "3.6", "topic": "chain_rule", "subject": "calculus"},
            },
            {
                "content": (
                    "Integration by parts is based on the product rule for differentiation and is used "
                    "to integrate products of functions. The formula is ∫u dv = uv − ∫v du. "
                    "The key skill is choosing u and dv wisely. The LIATE rule (Logarithmic, Inverse trig, "
                    "Algebraic, Trigonometric, Exponential) provides a guideline for choosing u — pick the "
                    "function type that appears earliest in the LIATE list."
                ),
                "metadata": {"source": "openstax_calculus", "chapter": "5", "section": "5.1", "topic": "integration_by_parts", "subject": "calculus"},
            },
            {
                "content": (
                    "The Fundamental Theorem of Calculus has two parts. Part 1 states that if f is continuous "
                    "on [a, b] and F(x) = ∫ₐˣ f(t) dt, then F'(x) = f(x). Part 2 states that if F is any "
                    "antiderivative of f on [a, b], then ∫ₐᵇ f(x) dx = F(b) − F(a). Together, these parts "
                    "establish that differentiation and integration are inverse operations."
                ),
                "metadata": {"source": "openstax_calculus", "chapter": "5", "section": "5.3", "topic": "fundamental_theorem", "subject": "calculus"},
            },
        ]
