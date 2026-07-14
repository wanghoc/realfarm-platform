"""Harvests module router.

The player's harvest entitlement MUST be linked to the active lease and crop cycle.
Unsafe or contaminated produce MUST NOT be delivered.
Withdrawal period blocking MUST be enforced.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import TokenPayload, get_current_user

router = APIRouter(prefix="/harvests", tags=["harvests"])


@router.get("")
async def list_harvests(current_user: Annotated[TokenPayload, Depends(get_current_user)]) -> list:
    """List harvest records for the current player. TODO: implement."""
    return []


@router.get("/{harvest_id}/entitlement")
async def get_harvest_entitlement(
    harvest_id: str, current_user: Annotated[TokenPayload, Depends(get_current_user)]
) -> dict:
    """Get harvest entitlement details linked to player lease. TODO: implement."""
    return {"harvest_id": harvest_id, "status": "placeholder"}
