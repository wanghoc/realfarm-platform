"""Contract tests for the action policy engine interface (issue #107).

These pin the shape the whole policy layer depends on: the six policy results named
in ``docs/15_ACTION_CATALOG.md`` §2, the abstractness of ``ActionPolicyEngine``, and
the fact that a decision always carries a result and a reason. If any of these drift
from the catalog the test fails here, in CI, not in a hand-run script.
"""

import pytest
from pydantic import ValidationError

from app.modules.player_actions.api.router import PolicyDecision as RouterPolicyDecision
from app.modules.player_actions.application.policy import (
    ActionPolicyEngine,
    ActionRequest,
    PolicyDecision,
    PolicyResult,
)

# The authoritative set from docs/15_ACTION_CATALOG.md §2.
_EXPECTED_RESULTS = {
    "accepted_for_automation",
    "accepted_for_work_order",
    "scheduled",
    "rejected",
    "requires_expert_review",
    "expired",
}


def test_policy_result_is_exactly_the_six_catalog_values() -> None:
    assert {r.value for r in PolicyResult} == _EXPECTED_RESULTS


def test_router_and_engine_share_one_policy_decision() -> None:
    """The router returns the same PolicyDecision the engine produces — no second copy."""
    assert RouterPolicyDecision is PolicyDecision


def test_engine_interface_is_abstract() -> None:
    """ActionPolicyEngine is a contract, not something you can instantiate directly."""
    with pytest.raises(TypeError):
        ActionPolicyEngine()  # type: ignore[abstract]


def test_decision_requires_result_and_reason() -> None:
    ok = PolicyDecision(result=PolicyResult.rejected, reason="soil already moist")
    assert ok.result is PolicyResult.rejected
    assert ok.reason

    with pytest.raises(ValidationError):
        PolicyDecision(result=PolicyResult.rejected)  # type: ignore[call-arg]  # reason missing


def test_action_request_carries_plot_action_and_player() -> None:
    req = ActionRequest(
        plot_id="plot-1", action_type="request_extra_watering", player_id="player-1"
    )
    assert (req.plot_id, req.action_type, req.player_id) == (
        "plot-1",
        "request_extra_watering",
        "player-1",
    )
    assert req.parameters is None
