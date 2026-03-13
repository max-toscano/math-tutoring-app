"""
subject_resolver.py
Determines which subject module should handle the student's request.

Responsibility:
    If the caller specifies a subject, use it directly.
    Otherwise, inspect the student's input for subject keywords
    and return the best match. Defaults to "math" when uncertain.
"""

# Keyword map: subject -> trigger words
_SUBJECT_KEYWORDS: dict[str, list[str]] = {
    "math": [
        "equation", "solve", "algebra", "calculus", "geometry",
        "fraction", "integral", "derivative", "triangle", "graph",
        "number", "formula", "variable", "polynomial",
    ],
    "chemistry": [
        "element", "molecule", "atom", "reaction", "compound",
        "periodic", "bond", "acid", "base", "solution", "mole",
    ],
    "physics": [
        "force", "velocity", "acceleration", "mass", "energy",
        "gravity", "momentum", "newton", "wave", "circuit", "charge",
    ],
    "biology": [
        "cell", "dna", "organism", "evolution", "photosynthesis",
        "protein", "gene", "species", "ecosystem", "membrane",
    ],
}


def resolve_subject(
    student_input: str,
    requested_subject: str | None = None,
) -> str:
    """
    Resolve the subject for a tutoring request.

    Args:
        student_input:      The raw text from the student.
        requested_subject:  Optional explicit subject from the API request.

    Returns:
        A subject string: "math", "chemistry", "physics", "biology",
        or "math" as the default fallback.
    """
    # Caller explicitly specified a subject — trust it.
    if requested_subject:
        return requested_subject.lower().strip()

    # Keyword-based detection.
    lowered = student_input.lower()
    for subject, keywords in _SUBJECT_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return subject

    # TODO: Replace keyword matching with an LLM-based classifier.
    return "math"
