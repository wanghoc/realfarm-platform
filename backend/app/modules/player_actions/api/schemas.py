"""Transport and policy schemas for the player_actions module.

The policy engine turns a player action REQUEST into exactly one outcome plus a
human-readable reason (ADR-0003; ``docs/15_ACTION_CATALOG.md`` §2). ``PolicyOutcome``
is the single source of truth for the six outcomes — the router and the engine both
import it so the set cannot drift.
"""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel

from app.core.schema import CamelModel


class PolicyOutcome(StrEnum):
    """The six results a policy evaluation may return.

    Matches ``docs/02_BUSINESS_RULES.md`` (Player actions) and
    ``docs/15_ACTION_CATALOG.md`` §2.
    """

    accepted_for_automation = "accepted_for_automation"
    accepted_for_work_order = "accepted_for_work_order"
    scheduled = "scheduled"
    rejected = "rejected"
    requires_expert_review = "requires_expert_review"
    expired = "expired"


class ActionCategory(StrEnum):
    """How far a player is allowed to drive an action (``docs/15_ACTION_CATALOG.md`` §3).

    Defined ahead of use: the policy engine consumes it in Weeks 7-8. Not yet
    referenced elsewhere (scaffold).
    """

    automation_eligible = "automation_eligible"  # A — policy may execute within limits
    manual_work = "manual_work"  # B — always becomes a work order
    restricted = "restricted"  # C — expert/operator only, never player-driven automation
    other_module = "other_module"  # D — handled by commerce/media, not the IoT policy engine


class ActionRequestBody(BaseModel):
    """Minimal request body accepted by the submit endpoint today (scaffold).

    The full policy input is ``PlayerActionRequestV1``; this narrower body is what the
    stub endpoint parses until the submit flow is wired in Weeks 7-8.
    """

    plot_id: str
    action_type: str  # e.g. "water", "inspect", "nutrient_check"
    notes: str | None = None


class PlayerActionRequestV1(CamelModel):
    """The policy engine's input — mirrors ``player-action-request.v1.json``."""

    request_id: str
    player_id: str
    lease_id: str
    plot_id: str
    crop_cycle_id: str
    action_type: str
    requested_at: datetime
    parameters: dict | None = None
    idempotency_key: str | None = None


class PolicyDecision(BaseModel):
    """The engine's output: one outcome, always with a human-readable reason.

    ``policy_version`` records which action-policy version decided this, so the
    decision can be reconstructed later (ADR-0003 consequence).
    """

    result: PolicyOutcome
    reason: str
    policy_version: int | None = None
