"""
JWT security utilities, password hashing, and refresh token helpers.

Design:
- Access tokens are short-lived JWTs signed with HS256.
- Refresh tokens are cryptographically random opaque strings.
- Only the SHA-256 hash of a refresh token is stored in the DB.
"""

import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Annotated

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import settings

# ── Password hashing ──────────────────────────────────────────────────────────


def hash_password(plain: str) -> str:
    """Return the bcrypt hash of a plain-text password."""
    pwd_bytes = plain.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    """Return True when the plain password matches the stored bcrypt hash."""
    try:
        pwd_bytes = plain.encode("utf-8")
        hashed_bytes = hashed.encode("utf-8")
        return bcrypt.checkpw(pwd_bytes, hashed_bytes)
    except Exception:
        return False


# ── Access Token (JWT) ────────────────────────────────────────────────────────

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class TokenPayload(BaseModel):
    sub: str  # user id
    role: str
    exp: datetime


def create_access_token(user_id: str, role: str) -> str:
    """Create a signed JWT access token valid for the configured duration."""
    expire = datetime.now(UTC) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "role": role, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> TokenPayload:
    """Decode and validate a JWT. Raises HTTP 401 on any failure."""
    try:
        raw = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return TokenPayload(**raw)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenPayload:
    """FastAPI dependency: validate JWT and return the payload."""
    return decode_token(token)


def require_role(*roles: str):
    """Dependency factory: only allow users with one of the specified roles."""

    async def _guard(payload: Annotated[TokenPayload, Depends(get_current_user)]) -> TokenPayload:
        if payload.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role: {', '.join(roles)}",
            )
        return payload

    return _guard


# ── Refresh Token (opaque) ────────────────────────────────────────────────────

REFRESH_TOKEN_BYTES = 64  # 512-bit entropy


def generate_refresh_token() -> str:
    """
    Generate a cryptographically secure random refresh token string.
    This plain value is returned to the client and MUST NOT be stored as-is.
    """
    return secrets.token_urlsafe(REFRESH_TOKEN_BYTES)


def hash_refresh_token(plain: str) -> str:
    """Return the SHA-256 hex digest of the plain refresh token for DB storage."""
    return hashlib.sha256(plain.encode()).hexdigest()
