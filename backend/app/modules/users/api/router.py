"""Users module router — user profile management."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import TokenPayload, get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def get_current_user_profile(
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
) -> dict:
    """Return the authenticated user's profile. TODO: load from DB."""
    return {"id": current_user.sub, "role": current_user.role}
