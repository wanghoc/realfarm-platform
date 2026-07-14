"""Crop cycles module router."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import TokenPayload, get_current_user

router = APIRouter(prefix="/crop-cycles", tags=["crop-cycles"])


@router.get("")
async def list_crop_cycles(
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
) -> list:
    """List crop cycles for the current user's plots. TODO: implement."""
    return []


@router.get("/{cycle_id}")
async def get_crop_cycle(
    cycle_id: str, current_user: Annotated[TokenPayload, Depends(get_current_user)]
) -> dict:
    """Get crop cycle details including growth stage and health summary. TODO: implement."""
    return {"id": cycle_id, "status": "placeholder"}
