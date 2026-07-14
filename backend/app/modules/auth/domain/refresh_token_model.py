"""
RefreshToken ORM model.

Security design:
- The plain token string is NEVER stored in the database.
- Only a SHA-256 hash of the token is stored (token_hash).
- This means a DB breach does not expose usable refresh tokens.
- Each refresh rotates: old token is revoked, a new pair is issued.
- Tokens can be revoked per-device or all at once (by deleting all for a user).
"""

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.modules.auth.domain.user_model import User


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    user_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # SHA-256 hash of the plain token sent to the client
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    is_revoked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # Optional: record the device/user-agent for per-device revocation
    device_hint: Mapped[str | None] = mapped_column(String(255), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="refresh_tokens")

    __table_args__ = (Index("ix_refresh_tokens_token_hash", "token_hash"),)

    @property
    def is_valid(self) -> bool:
        """A token is valid when it is not revoked and has not expired."""
        return not self.is_revoked and datetime.now(UTC) < self.expires_at

    def __repr__(self) -> str:
        return f"<RefreshToken id={self.id} user_id={self.user_id} revoked={self.is_revoked}>"
