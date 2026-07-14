"""
Login use-case: authenticate user credentials and issue access + refresh tokens.

Flow:
1. Look up user by email.
2. Verify the bcrypt password hash.
3. Generate a new access token (JWT) and a new refresh token (opaque).
4. Hash and persist the refresh token in the database.
5. Return the plain tokens to the caller (API layer formats the response).
"""

from datetime import UTC, datetime, timedelta
from typing import NamedTuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_refresh_token,
    verify_password,
)
from app.modules.auth.domain.refresh_token_model import RefreshToken
from app.modules.auth.domain.user_model import User


class LoginResult(NamedTuple):
    access_token: str
    refresh_token: str
    user: User


async def login_user(email: str, password: str, db: AsyncSession) -> LoginResult:
    """
    Authenticate a user and return a fresh token pair.

    Raises ValueError with a generic message on any auth failure
    (intentionally vague to avoid user-enumeration attacks).
    """
    # 1. Look up user by email
    result = await db.execute(select(User).where(User.email == email, User.is_active == True))  # noqa: E712
    user = result.scalar_one_or_none()

    if user is None or not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")

    # 2. Create access token (JWT)
    access_token = create_access_token(user_id=user.id, role=user.role)

    # 3. Create opaque refresh token
    plain_refresh = generate_refresh_token()
    token_hash = hash_refresh_token(plain_refresh)
    expires_at = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    refresh_token_entity = RefreshToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
    )
    db.add(refresh_token_entity)
    await db.flush()  # persist within the caller's transaction

    return LoginResult(
        access_token=access_token,
        refresh_token=plain_refresh,
        user=user,
    )
