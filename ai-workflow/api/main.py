"""
main.py
FastAPI application entry point.

Run with:
    uvicorn api.main:app --reload
"""

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import init_db
from api.routes import auth, tutor, progress, saved

app = FastAPI(
    title="AI Tutoring API",
    description="Backend for the multi-subject AI tutoring app.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tutor.router)
app.include_router(progress.router)
app.include_router(saved.router)


@app.on_event("startup")
def on_startup():
    init_db()
