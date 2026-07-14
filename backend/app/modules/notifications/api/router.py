"""Notifications module router."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import TokenPayload, get_current_user

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("")
async def list_notifications(
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
) -> list:
    """List notifications for the current user. TODO: implement."""
    return []


@router.post("/{notification_id}/read")
async def mark_read(
    notification_id: str, current_user: Annotated[TokenPayload, Depends(get_current_user)]
) -> dict:
    """Mark notification as read. TODO: implement."""
    return {"notification_id": notification_id, "read": True}
