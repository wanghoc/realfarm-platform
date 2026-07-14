"""Deliveries module router."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import TokenPayload, get_current_user

router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.post("")
async def request_delivery(
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
) -> dict:
    """Request pickup or delivery for a harvest entitlement. TODO: implement."""
    return {"status": "placeholder"}
