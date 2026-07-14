"""Leases module router.

Business rules enforced here:
- A plot MUST NOT have more than one active lease at the same time.
- Lease activation MUST fail when the plot is unavailable.
- A player MUST only access leases they own.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import TokenPayload, get_current_user

router = APIRouter(prefix="/leases", tags=["leases"])


@router.get("")
async def list_my_leases(current_user: Annotated[TokenPayload, Depends(get_current_user)]) -> list:
    """List leases belonging to the current player. TODO: implement."""
    return []


@router.post("")
async def create_lease(current_user: Annotated[TokenPayload, Depends(get_current_user)]) -> dict:
    """Submit a lease request. TODO: implement with plot availability check."""
    return {"status": "placeholder"}


@router.post("/{lease_id}/activate")
async def activate_lease(
    lease_id: str, current_user: Annotated[TokenPayload, Depends(get_current_user)]
) -> dict:
    """Activate a pending lease. TODO: implement state machine transition."""
    return {"lease_id": lease_id, "status": "placeholder"}
