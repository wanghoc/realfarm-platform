"""Player action requests module router.

A player action is always a REQUEST. The policy engine evaluates it and returns exactly
one outcome plus a human-readable reason (ADR-0003; ``docs/15_ACTION_CATALOG.md``). The
six outcomes live in ``PolicyOutcome`` (see api/schemas.py) so the router, the engine,
and the catalog cannot drift apart.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import TokenPayload, get_current_user
from app.modules.player_actions.api.schemas import ActionRequestBody, PolicyDecision, PolicyOutcome

router = APIRouter(prefix="/player-action-requests", tags=["player-actions"])


@router.post("")
async def submit_action_request(
    body: ActionRequestBody,
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
) -> PolicyDecision:
    """
    Submit a player action request.
    The policy engine evaluates and returns a decision.
    TODO: wire ActionPolicyEngine.evaluate() (Weeks 7-8) and work-order creation.
    """
    return PolicyDecision(
        result=PolicyOutcome.scheduled,
        reason="Scaffold placeholder — policy engine not yet implemented.",
    )


@router.get("")
async def list_my_action_requests(
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
) -> list:
    """List the current player's action requests. TODO: implement."""
    return []


@router.post("/{request_id}/cancel")
async def cancel_action_request(
    request_id: str, current_user: Annotated[TokenPayload, Depends(get_current_user)]
) -> dict:
    """Cancel a pending action request. TODO: implement."""
    return {"request_id": request_id, "status": "placeholder"}
