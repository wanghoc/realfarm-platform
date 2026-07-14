"""Admin module router."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import TokenPayload, require_role

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users")
async def list_all_users(
    current_user: Annotated[TokenPayload, Depends(require_role("admin"))],
) -> list:
    """Admin: list all users. TODO: implement."""
    return []
