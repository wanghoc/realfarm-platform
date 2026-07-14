"""Incidents module router.

Crop failure MUST create an incident record.
A replacement plot/crop MUST require customer notification.
Historical records MUST remain accessible after replacement.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import TokenPayload, get_current_user

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.get("")
async def list_incidents(current_user: Annotated[TokenPayload, Depends(get_current_user)]) -> list:
    """List incidents. TODO: implement with role-based filtering."""
    return []
