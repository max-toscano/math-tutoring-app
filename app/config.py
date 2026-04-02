"""
config.py
Application settings loaded from environment variables.
Single source of truth for all configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the app directory (works regardless of working directory)
_env_path = Path(__file__).parent / ".env"
load_dotenv(_env_path)

# ── LLM ───────────────────────────────────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# ── Database ──────────────────────────────────────────────────────────────
DATABASE_URL = os.getenv("DATABASE_URL")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# ── RAG / Vector Store ────────────────────────────────────────────────────
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "./data/vectorstore")
OPENSTAX_DATA_PATH = os.getenv("OPENSTAX_DATA_PATH", "./data/openstax")

# ── Embedding ─────────────────────────────────────────────────────────────
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

# ── Google Custom Search ──────────────────────────────────────────────────
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

# ── Dev Mode ──────────────────────────────────────────────────────────────
DEV_MODE = os.getenv("DEV_MODE", "true").lower() == "true"
