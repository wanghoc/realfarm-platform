"""Action policy engine interface.

A player action is a REQUEST, never a direct actuator command (ADR-0003;
``docs/15_ACTION_CATALOG.md`` §1). This module defines the interface a concrete engine
implements and the decision type it returns. Concrete engines live alongside this file
(e.g. the watering policy, issue #124); the engine that reads live sensors and versioned
policies lands with the telemetry/automation slice in Weeks 7-8
(``docs/10_ROADMAP_16_WEEKS.md``).

``PolicyResult`` and ``PolicyDecision`` are defined here, in the application layer that
produces them, and imported by the API router that returns them — a single source of
truth so the router's response shape and the engine's output cannot drift apart.
"""

from abc import ABC, abstractmethod
from enum import StrEnum

from pydantic import BaseModel


class PolicyResult(StrEnum):
    """The six outcomes a policy evaluation may return (``docs/15_ACTION_CATALOG.md`` §2).

    Exactly one is returned per request, always with a human-readable reason. Matches
    ``docs/02_BUSINESS_RULES.md`` (Player actions).
    """

    accepted_for_automation = "accepted_for_automation"
    accepted_for_work_order = "accepted_for_work_order"
    scheduled = "scheduled"
    rejected = "rejected"
    requires_expert_review = "requires_expert_review"
    expired = "expired"


class ActionRequest(BaseModel):
    """What the engine evaluates: who asked for what, on which plot.

    The full wire contract is ``packages/contracts/schemas/player-action-request.v1.json``;
    this is the minimal application-level view the engine needs. ``player_id`` is the
    authenticated actor (the API layer fills it from the token, not the request body).
    """

    plot_id: str
    action_type: str
    player_id: str
    parameters: dict | None = None


class PolicyDecision(BaseModel):
    """The engine's output: exactly one result plus a human-readable reason.

    ``reason`` is mandatory for every outcome (``docs/15_ACTION_CATALOG.md`` §2) so a
    rejection or deferral can always be explained back to the player.
    """

    result: PolicyResult
    reason: str


class ActionPolicyEngine(ABC):
    """Evaluates a player action request into exactly one ``PolicyDecision``.

    Contract (``docs/15_ACTION_CATALOG.md``, ``docs/02_BUSINESS_RULES.md``):

    - every request returns exactly one ``PolicyResult`` and a non-empty reason;
    - an unknown ``action_type`` MUST be rejected with a clear reason;
    - a restricted Category C action MUST NOT return ``accepted_for_automation`` — a
      player can never directly drive pesticide use, destructive pruning, crop removal,
      or unsafe actuator duration; safety automation overrides player preference
      (``AGENTS.md`` §2). Such actions are routed to expert review or rejected.
    """

    @abstractmethod
    async def evaluate(self, request: ActionRequest) -> PolicyDecision:
        """Return the policy decision for one request."""
        raise NotImplementedError
