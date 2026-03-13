"""
topic_router.py
Classifies an incoming math question into a specific topic area.
Allows future logic to apply topic-specific strategies and rules.
"""

# Keyword map: topic name -> list of trigger words
_TOPIC_KEYWORDS: dict[str, list[str]] = {
    "algebra": ["equation", "variable", "solve", "expression", "polynomial", "factor", "inequality"],
    "geometry": ["angle", "triangle", "circle", "area", "perimeter", "volume", "shape", "polygon"],
    "calculus": ["derivative", "integral", "limit", "differentiate", "integrate", "rate of change"],
    "trigonometry": ["sin", "cos", "tan", "sine", "cosine", "tangent", "radian", "hypotenuse"],
    "statistics": ["mean", "median", "mode", "probability", "distribution", "variance", "standard deviation"],
}


def route_math_topic(question: str) -> str:
    """
    Classify a math question into a topic based on keyword matching.
    Returns a topic string such as 'algebra', 'geometry', or 'general_math'.
    """
    lowered = question.lower()

    for topic, keywords in _TOPIC_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return topic

    # TODO: Replace keyword matching with an AI-based classifier when ready.
    return "general_math"
