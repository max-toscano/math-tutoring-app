"""
api/middleware/auth.py
Validates Supabase JWT tokens from the Authorization header.
Extracts student_id (sub claim) for use in route handlers.

Uses ES256 (asymmetric) JWT signing with Supabase's JWKS endpoint.
"""

from uuid import UUID

import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import SUPABASE_URL, SUPABASE_ANON_KEY, DEV_MODE

security = HTTPBearer(auto_error=False)

# Initialize JWKS client if Supabase is configured
_jwks_client = None
if SUPABASE_URL and SUPABASE_ANON_KEY:
    jwks_url = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"
    _jwks_client = PyJWKClient(
        jwks_url,
        cache_jwk_set=True,
        lifespan=300,
        headers={"apikey": SUPABASE_ANON_KEY},
    )


def get_current_student_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    FastAPI dependency — decodes the Supabase JWT and returns the student's ID as text.

    Returns the UUID as a string to match student_profiles.student_id (text column).

    If no auth is configured (development mode), returns a test student ID.
    """
    # Development mode — skip auth, use test student
    if DEV_MODE or not _jwks_client:
        return "test_student_001"

    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    token = credentials.credentials
    try:
        signing_key = _jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["ES256"],
            audience="authenticated",
        )
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing 'sub' claim",
            )
        return str(sub)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
        )
