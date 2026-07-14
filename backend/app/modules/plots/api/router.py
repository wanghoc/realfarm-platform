"""Plots module router."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import TokenPayload, get_current_user

router = APIRouter(prefix="/plots", tags=["plots"])


@router.get("")
async def list_plots(current_user: Annotated[TokenPayload, Depends(get_current_user)]) -> list:
    """
    List plots available for lease.
    Players see available plots. Operators see all plots in their farm.
    TODO: implement with DB query and role-based filtering.
    """
    return []


@router.get("/{plot_id}")
async def get_plot(
    plot_id: str, current_user: Annotated[TokenPayload, Depends(get_current_user)]
) -> dict:
    """Get single plot details. TODO: implement."""
    return {"id": plot_id, "status": "placeholder"}
