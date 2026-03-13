"""
main.py
FastAPI application entry point for the ai-workflow service.

Responsibility:
    Creates the FastAPI app instance and mounts all routers.
    This file is the top-level entry point — it contains no business logic.

Architecture:
    main.py → router.py → tutor_engine.py → tutoring/subjects/math/

Run with:
    uvicorn api.main:app --reload
"""

from fastapi import FastAPI
from .router import router

app = FastAPI(
    title="AI Tutoring API",
    description="API layer for the AI tutoring workflow.",
    version="0.1.0",
)

app.include_router(router)
