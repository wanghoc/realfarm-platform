"""Seed a demo user on first startup (development only)."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.modules.auth.domain.user_model import User


async def seed_demo_user(db: AsyncSession) -> None:
    """
    Insert a demo player account if it does not already exist.
    Only runs when APP_ENV == 'development'.
    """
    result = await db.execute(select(User).where(User.email == "demo@realfarm.dev"))
    if result.scalar_one_or_none() is not None:
        return  # Already seeded

    demo = User(
        email="demo@realfarm.dev",
        password_hash=hash_password("demo1234"),
        full_name="Demo Player",
        role="player",
    )
    db.add(demo)
    await db.flush()
