"""
auth_middleware.py
Validates Supabase JWT tokens from the Authorization header.
Extracts user_id (sub claim) for use in route handlers.

This project uses ES256 (asymmetric) JWT signing, so we verify tokens
using the public key from Supabase's JWKS endpoint.
"""

import os
from uuid import UUID

import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL environment variable is required")
if not SUPABASE_ANON_KEY:
    raise RuntimeError("SUPABASE_ANON_KEY environment variable is required")

# Fetch signing keys from Supabase's JWKS endpoint (cached for 5 min)
jwks_url = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"
jwks_client = PyJWKClient(
    jwks_url,
    cache_jwk_set=True,
    lifespan=300,
    headers={"apikey": SUPABASE_ANON_KEY},
)


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UUID:
    """
    FastAPI dependency — decodes the Supabase JWT and returns the user's UUID.
    Usage in routes: user_id: UUID = Depends(get_current_user_id)
    """
    token = credentials.credentials
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
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
        return UUID(sub)
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
