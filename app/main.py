"""
main.py
FastAPI application entry point.

Run with:
    uvicorn app.main:app --reload --port 8001
"""

from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes import chat

app = FastAPI(
    title="Math Tutoring API",
    description="AI math tutoring system with RAG, memory, and real math tools.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)

# Serve static files (chat UI)
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    """Serve the chat UI."""
    return FileResponse(str(static_dir / "chat.html"))
