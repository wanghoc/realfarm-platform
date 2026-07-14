"""Crop catalog module router."""

from fastapi import APIRouter

router = APIRouter(prefix="/crop-catalog", tags=["crop-catalog"])


@router.get("")
async def list_crops() -> list:
    """List crops available for selection. TODO: load from DB."""
    return []
