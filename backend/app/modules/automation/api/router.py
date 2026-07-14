"""Automation module router.

Commands to actuators MUST record: source, reason, target, requested duration,
actual duration, status, and timestamps.
Commands require idempotency keys.
Watchdog limits must be enforced.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import TokenPayload, require_role

router = APIRouter(prefix="/automation", tags=["automation"])


@router.get("/commands")
async def list_commands(
    current_user: Annotated[TokenPayload, Depends(require_role("operator", "admin"))],
) -> list:
    """List automation commands. Operator/admin only. TODO: implement."""
    return []
