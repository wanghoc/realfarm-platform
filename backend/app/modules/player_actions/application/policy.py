"""Action policy engine interface.

A player action is a request, never a direct actuator command (ADR-0003). This module
defines only the *interface* the concrete engine implements; the engine itself (reading
sensors, versioned action policies, package quotas, and safe windows) lands with the
telemetry/automation slice in Weeks 7-8 (``docs/10_ROADMAP_16_WEEKS.md``).
"""

from abc import ABC, abstractmethod

from app.modules.player_actions.api.schemas import PlayerActionRequestV1, PolicyDecision


class ActionPolicyEngine(ABC):
    """Evaluates a player action request into exactly one outcome and a reason.

    Contract (``docs/15_ACTION_CATALOG.md``, ``docs/02_BUSINESS_RULES.md``):

    - every request returns exactly one ``PolicyOutcome`` and a human-readable reason;
    - an unknown ``action_type`` MUST be rejected with a clear reason;
    - a restricted (Category C) action MUST NOT return ``accepted_for_automation`` —
      emergency safety automation overrides player preference (``AGENTS.md`` §2);
    - the deciding policy version MUST be recorded on the decision (ADR-0003), so an
      action can be reconstructed after the fact.
    """

    @abstractmethod
    async def evaluate(self, request: PlayerActionRequestV1) -> PolicyDecision:
        """Return the policy decision for one request. Implemented in Weeks 7-8."""
        raise NotImplementedError
