"""Farms module router."""

from fastapi import APIRouter

router = APIRouter(prefix="/farms", tags=["farms"])


@router.get("")
async def list_farms() -> list:
    """List all farms. TODO: load from DB with role-based filtering."""
    return []
