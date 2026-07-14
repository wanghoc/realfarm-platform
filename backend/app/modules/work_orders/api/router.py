"""Work orders module router.

Manual agricultural work MUST be represented by a work order.
Completion SHOULD include before/after evidence.
Missing evidence requires an explicit reason and reviewer approval.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import TokenPayload, get_current_user, require_role

router = APIRouter(prefix="/work-orders", tags=["work-orders"])


@router.get("")
async def list_work_orders(
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
) -> list:
    """
    List work orders.
    Operators see all assigned orders; players see customer-safe status only.
    TODO: implement with role-based view.
    """
    return []


@router.post("/{order_id}/complete")
async def complete_work_order(
    order_id: str,
    current_user: Annotated[TokenPayload, Depends(require_role("operator", "admin"))],
) -> dict:
    """Mark a work order complete. Requires evidence. TODO: implement."""
    return {"order_id": order_id, "status": "placeholder"}
