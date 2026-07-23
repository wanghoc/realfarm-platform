"""Player action requests module router.

A player action is always a REQUEST.
Policy result MUST be one of:
  accepted_for_automation | accepted_for_work_order |
  scheduled | rejected | requires_expert_review | expired

Response MUST include a human-readable reason.
"""

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.security import TokenPayload, get_current_user
from app.modules.player_actions.application.policy import PolicyDecision, PolicyResult

router = APIRouter(prefix="/player-action-requests", tags=["player-actions"])


class ActionRequestBody(BaseModel):
    plot_id: str
    action_type: str  # e.g. "water", "inspect", "nutrient_check"
    notes: str | None = None


@router.post("")
async def submit_action_request(
    body: ActionRequestBody,
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
) -> PolicyDecision:
    """
    Submit a player action request.
    The policy engine evaluates and returns a decision.
    TODO: implement policy engine and work-order creation.
    """
    return PolicyDecision(
        result=PolicyResult.scheduled,
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
