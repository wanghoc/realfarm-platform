"""
Refresh token use-case: rotate tokens.

Flow:
1. Hash the incoming plain refresh token.
2. Look up a matching, non-revoked, non-expired record in the DB.
3. Revoke the old token (rotation — prevents replay attacks).
4. Issue a new access token + new refresh token.
5. Persist the new refresh token hash.
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
)
from app.modules.auth.domain.refresh_token_model import RefreshToken
from app.modules.auth.domain.user_model import User


class RefreshResult(NamedTuple):
    access_token: str
    refresh_token: str


async def refresh_tokens(plain_token: str, db: AsyncSession) -> RefreshResult:
    """
    Exchange a valid refresh token for a new token pair.

    Raises ValueError when the token is invalid, expired, or revoked.
    The old token is revoked regardless of outcome (rotation).
    """
    token_hash = hash_refresh_token(plain_token)

    # 1. Find the stored refresh token by its hash
    result = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
    stored = result.scalar_one_or_none()

    if stored is None or not stored.is_valid:
        raise ValueError("Refresh token is invalid, expired, or already revoked")

    # 2. Revoke the old token immediately (rotation)
    stored.is_revoked = True
    await db.flush()

    # 3. Load the user to embed their current role in the new access token
    user_result = await db.execute(select(User).where(User.id == stored.user_id))
    user = user_result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise ValueError("User not found or deactivated")

    # 4. Issue new tokens
    new_access_token = create_access_token(user_id=user.id, role=user.role)
    new_plain_refresh = generate_refresh_token()
    new_hash = hash_refresh_token(new_plain_refresh)
    new_expires = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    new_refresh_entity = RefreshToken(
        user_id=user.id,
        token_hash=new_hash,
        expires_at=new_expires,
    )
    db.add(new_refresh_entity)
    await db.flush()

    return RefreshResult(access_token=new_access_token, refresh_token=new_plain_refresh)
