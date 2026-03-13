"""
orchestrator package

Coordinates subject modules and mode modules to produce tutoring responses.
The orchestrator sits between the API layer and the tutoring knowledge layer.

Public API:
    generate_tutoring_response — the single entry point called by the API router.
"""

from .tutor_engine import generate_tutoring_response

__all__ = ["generate_tutoring_response"]
