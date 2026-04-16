"""
main.py
FastAPI application entry point.

Run with:
    uvicorn app.main:app --reload --port 8001

── CORS (Cross-Origin Resource Sharing) ──────────────────────────────────────

WHAT IS CORS?
When your frontend (http://localhost:8081) makes a fetch() request to your
backend (http://localhost:8001), the BROWSER notices these are different
"origins" (different port = different origin). By default, browsers BLOCK
these cross-origin requests to protect users.

CORS is how your backend says: "These specific websites are allowed to
call me." The browser enforces this — NOT your backend.

HOW IT WORKS (step by step):
1. Your frontend JS runs: fetch("http://localhost:8001/chat/message", ...)
2. Browser sees it's a cross-origin request (port 8081 → port 8001)
3. Browser sends a "preflight" OPTIONS request first, with the header:
       Origin: http://localhost:8081
4. Your backend checks: is that origin in my ALLOWED_ORIGINS list?
   - YES → responds with: Access-Control-Allow-Origin: http://localhost:8081
   - NO  → responds without that header
5. Browser reads the response:
   - Has the allow header → sends the real POST request
   - Missing the header → BLOCKS the request, JS gets a CORS error

WHY ["*"] IS DANGEROUS:
allow_origins=["*"] means ANY website can call your API. Imagine someone
makes evil-site.com. If your user visits that site while logged into
MathHelper, evil-site.com's JavaScript can call YOUR API using the user's
auth token. The browser would allow it because you said "*" (everyone).

IMPORTANT: CORS only applies to BROWSERS (web). Your React Native app
running on a phone makes direct HTTP requests — no preflight, no CORS.
So this only matters for Expo Web and any future web deployment.
"""

import os
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

# ── ALLOWED_ORIGINS ─────────────────────────────────────────────────────────
#
# List every "origin" your frontend runs on. An origin = scheme + host + port.
#     http://localhost:8081   and   http://localhost:8082
# are DIFFERENT origins (different port).
#
# How to figure out what to put here:
#   1. Open your frontend in a browser
#   2. Look at the URL bar — that's the origin
#   3. Add it to this list
#
# When you deploy to production, add your real domain here too.
# If you forget, your deployed frontend won't be able to talk to the backend
# (you'll see CORS errors in the browser console).
#
ALLOWED_ORIGINS = [
    "http://localhost:8081",       # Expo web dev server (default port)
    "http://localhost:19006",      # Expo web alternate dev port
    "http://localhost:8001",       # Backend itself (for the built-in chat.html UI)
]

# For phone/tablet testing on the same WiFi network, set LOCAL_IP in your .env:
#   LOCAL_IP=192.168.1.X   (run `ipconfig` on Windows or `ifconfig` on Mac to find yours)
# This avoids CORS errors when the Expo app runs on a physical device.
_local_ip = os.getenv("LOCAL_IP")
if _local_ip:
    ALLOWED_ORIGINS.append(f"http://{_local_ip}:8081")
    ALLOWED_ORIGINS.append(f"http://{_local_ip}:19006")

# On Railway (or any deployment), set ALLOWED_ORIGIN env var to your frontend URL.
# Railway auto-sets RAILWAY_PUBLIC_DOMAIN for you.
# Example: ALLOWED_ORIGIN=https://mathhelper.yourdomain.com
_extra_origin = os.getenv("ALLOWED_ORIGIN")
if _extra_origin:
    ALLOWED_ORIGINS.append(_extra_origin)

_railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
if _railway_domain:
    ALLOWED_ORIGINS.append(f"https://{_railway_domain}")

app.add_middleware(
    CORSMiddleware,

    # allow_origins: Which websites can call your API.
    #   Before: ["*"]  → any website on the internet (dangerous)
    #   After:  only YOUR frontends listed above
    allow_origins=ALLOWED_ORIGINS,

    # allow_credentials: Can the browser send cookies / Authorization headers?
    #   True = yes, the browser can include the "Authorization: Bearer <jwt>"
    #   header with requests. You need this because your frontend sends the
    #   JWT token to authenticate.
    #
    #   NOTE: When allow_origins is ["*"], browsers actually IGNORE credentials
    #   (it's a browser security rule). So the old config was secretly broken
    #   for credentialed requests on some browsers.
    allow_credentials=True,

    # allow_methods: Which HTTP methods can the frontend use?
    #   Before: ["*"]  → GET, POST, PUT, DELETE, PATCH, OPTIONS, etc.
    #   After:  only the methods your API actually uses.
    #
    #   Your app only needs:
    #     GET  → /health, / (serving the chat UI)
    #     POST → /chat/start-session, /chat/message, /chat/close-session
    #   No PUT, DELETE, or PATCH endpoints exist, so don't allow them.
    allow_methods=["GET", "POST"],

    # allow_headers: Which HTTP headers can the frontend send?
    #   Before: ["*"]  → any header at all
    #   After:  only the headers your frontend actually sends.
    #
    #   Your frontend sends two custom headers:
    #     "Authorization"  → carries the JWT: "Bearer eyJ..."
    #     "Content-Type"   → tells the server it's JSON: "application/json"
    #   That's it. No need to allow anything else.
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(chat.router)

# Serve static files (chat UI) — only mount if the directory has files
static_dir = Path(__file__).parent / "static"
if static_dir.exists() and any(static_dir.iterdir()):
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    """Root endpoint — serves chat UI if available, otherwise health check."""
    chat_html = static_dir / "chat.html"
    if chat_html.exists():
        return FileResponse(str(chat_html))
    return {"status": "ok", "app": "Math Tutoring API", "docs": "/docs"}
