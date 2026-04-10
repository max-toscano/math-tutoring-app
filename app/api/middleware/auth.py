"""
api/middleware/auth.py
Validates AWS Cognito JWT tokens from the Authorization header.
Extracts the student_id (the `sub` claim) for use in route handlers.

Cognito signs its JWTs with RS256 (RSA asymmetric signing). We fetch the
public keys from Cognito's public JWKS endpoint to verify signatures —
we never need a shared secret, because asymmetric crypto means anyone
can *verify* a token, but only Cognito can *sign* one.
"""

# UUID imported for type-hinting / future use. Cognito's `sub` claim is
# already a UUID string, so we simply return it as-is.
from uuid import UUID

# PyJWT is the library that decodes and verifies JWTs.
# `jwt` is the top-level module; `PyJWKClient` is a helper that fetches
# and caches the JSON Web Key Set (JWKS) — the public keys used to
# verify RS256 signatures.
import jwt
from jwt import PyJWKClient

# FastAPI's `Depends` lets us inject this function as a dependency into
# route handlers. `HTTPException` + `status` give standard HTTP errors.
from fastapi import Depends, HTTPException, status

# `HTTPBearer` is a FastAPI security scheme that reads the
# `Authorization: Bearer <token>` header. `auto_error=False` means it
# will NOT automatically raise if the header is missing — we handle
# that ourselves so DEV_MODE can bypass auth entirely.
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Pull Cognito settings from our central config module. Keeping config
# in one place (app/config.py) makes it trivial to swap environments.
from app.config import (
    COGNITO_USER_POOL_ID,
    COGNITO_REGION,
    COGNITO_CLIENT_ID,
    DEV_MODE,
)

# `security` is the FastAPI dependency object that actually extracts the
# bearer token from incoming requests. We inject it below via Depends().
security = HTTPBearer(auto_error=False)

# ─────────────────────────────────────────────────────────────────────
# JWKS client initialization
# ─────────────────────────────────────────────────────────────────────
# JWKS = "JSON Web Key Set". It's a JSON document listing the public
# keys that a token issuer uses to sign its JWTs. Cognito publishes
# this at a well-known, PUBLIC URL per user pool — no auth required to
# fetch it because public keys are, by definition, safe to share.
#
# URL format is fixed by AWS:
#   https://cognito-idp.{region}.amazonaws.com/{userPoolId}/.well-known/jwks.json
#
# PyJWKClient fetches that JSON once, caches the keys in memory, and
# transparently picks the correct key for a given token based on the
# token's `kid` (key ID) header. Without caching we'd hit AWS on every
# request, which would be slow and rate-limited.
_jwks_client = None
if COGNITO_USER_POOL_ID and COGNITO_REGION:
    jwks_url = (
        f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com"
        f"/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"
    )
    _jwks_client = PyJWKClient(
        jwks_url,
        cache_jwk_set=True,  # keep keys in memory between requests
        lifespan=300,        # refresh the cached keys every 5 minutes
        # NOTE: no `headers=` argument here. Supabase's JWKS endpoint
        # required an apikey header, but Cognito's is fully public.
    )


def get_current_student_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    FastAPI dependency — decodes the Cognito ID token and returns the
    student's ID (a UUID string).

    The returned string matches `student_profiles.student_id` in the DB.

    Behavior:
      * In DEV_MODE (or if Cognito isn't configured), returns a fixed
        test student ID so local dev doesn't need real auth.
      * Otherwise, verifies the JWT signature against Cognito's public
        keys and enforces that this is an ID token issued to our app.
    """
    # ── Dev bypass ────────────────────────────────────────────────────
    # When running locally we often don't want to spin up real auth.
    # DEV_MODE is toggled via the DEV_MODE env var in app/config.py.
    # We also bypass if the JWKS client failed to init (missing env
    # vars), so a half-configured dev environment still works.
    if DEV_MODE or not _jwks_client:
        return "test_student_001"

    # If auth IS configured but the client sent no Authorization header,
    # fail fast with 401. `credentials` is None when the header is
    # absent (because we set auto_error=False on HTTPBearer above).
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    # `credentials.credentials` is the raw token string (everything
    # after "Bearer " in the header). Slightly awkward naming, but
    # that's how FastAPI's HTTPBearer exposes it.
    token = credentials.credentials

    try:
        # Step 1: Look at the token's header to find its `kid`, then
        # fetch the matching public key from our cached JWKS.
        # PyJWKClient handles all of this under the hood.
        signing_key = _jwks_client.get_signing_key_from_jwt(token)

        # Step 2: Verify + decode the token.
        #
        # algorithms=["RS256"]:
        #   Cognito signs with RS256 (RSA + SHA-256). This is asymmetric:
        #   Cognito holds a private key to sign, we hold the public key
        #   to verify. Contrast with Supabase, which used ES256 — same
        #   idea (asymmetric) but using elliptic-curve math instead of
        #   RSA. Pinning the algorithm list prevents "alg=none"
        #   downgrade attacks.
        #
        # options={"verify_aud": False}:
        #   Normally PyJWT enforces that the token's `aud` claim matches
        #   a value we provide. Cognito has a quirk here: ID tokens put
        #   the app client ID in `aud`, but ACCESS tokens put it in a
        #   separate `client_id` claim and have no `aud` at all. To keep
        #   this code explicit and uniform, we disable PyJWT's automatic
        #   audience check and verify `client_id` ourselves below. We
        #   also require token_use == "id", so only ID tokens are
        #   accepted.
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            options={"verify_aud": False},
        )

        # Step 3: Manual `token_use` check.
        #
        # Cognito issues TWO kinds of JWTs per login:
        #   - "id"     → an ID token, describing WHO the user is
        #                (what our API wants)
        #   - "access" → an access token, describing WHAT they can do
        #                (for calling Cognito APIs, e.g. password change)
        # Our API identifies users, so we only accept ID tokens. If we
        # accepted access tokens too, a compromised access token from a
        # different scope could impersonate the user here.
        if payload.get("token_use") != "id":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type (expected ID token)",
            )

        # Step 4: Manual client_id check.
        #
        # Every Cognito token embeds the app client ID it was issued to.
        # For ID tokens Cognito puts this in the `aud` claim; it also
        # appears as `client_id` in access tokens. We check `client_id`
        # (with an `aud` fallback) to reject tokens issued to a
        # *different* app client — e.g. a mobile app for another product
        # in the same user pool. Without this check, any token from any
        # client in our user pool would be accepted here.
        expected_client = COGNITO_CLIENT_ID
        token_client = payload.get("client_id") or payload.get("aud")
        if token_client != expected_client:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token was not issued for this application",
            )

        # Step 5: Extract the subject.
        #
        # `sub` is a standard JWT claim meaning "subject" — for Cognito
        # it's the user's immutable UUID in the user pool. It never
        # changes even if the user updates their email/username, which
        # is exactly why we use it as our stable `student_id`.
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing 'sub' claim",
            )
        return str(sub)

    # ── Specific error: expired token ─────────────────────────────────
    # Split out from the generic InvalidTokenError so the client gets a
    # clearer message (and could, e.g., trigger a silent refresh flow).
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    # ── Generic catch-all for any other JWT validation failure ────────
    # Bad signature, malformed token, wrong algorithm, etc.
    # We include the exception message in `detail` to aid debugging,
    # but in a hardened prod setup you may want to log `e` server-side
    # and return a generic "Invalid token" message to avoid leaking
    # internals to clients.
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}",
        )
