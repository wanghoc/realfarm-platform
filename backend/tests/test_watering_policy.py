"""Tests for the watering policy engine (issue #124).

Async ``evaluate`` is driven with ``asyncio.run`` to match the suite's convention
(``test_command_listeners.py``); the project pins no async pytest plugin.

Logic under test (``docs/15_ACTION_CATALOG.md`` §4.1):
- extra watering: granted only when soil needs it and was not just watered;
- skip watering: granted only when soil is not too dry — a dry plot rejects the skip
  because safety automation overrides the player's preference.
"""

import asyncio

import pytest

from app.modules.player_actions.application.policy import ActionRequest, PolicyResult
from app.modules.player_actions.application.watering_policy import (
    DRY_NEEDS_WATER_PCT,
    EXTRA_WATERING,
    SKIP_WATERING,
    WET_ENOUGH_PCT,
    PlotConditions,
    StaticPlotConditionProvider,
    WateringPolicyEngine,
)


def _decide(
    action_type: str,
    *,
    soil_moisture_pct: float | None,
    minutes_since_last_watering: float | None = None,
):
    """Evaluate one action against fixed conditions and return the decision."""
    engine = WateringPolicyEngine(
        StaticPlotConditionProvider(
            PlotConditions(
                soil_moisture_pct=soil_moisture_pct,
                minutes_since_last_watering=minutes_since_last_watering,
            )
        )
    )
    request = ActionRequest(plot_id="plot-1", action_type=action_type, player_id="player-1")
    return asyncio.run(engine.evaluate(request))


# --- request_extra_watering -------------------------------------------------


def test_extra_watering_accepted_when_soil_dry() -> None:
    d = _decide(EXTRA_WATERING, soil_moisture_pct=20.0)
    assert d.result is PolicyResult.accepted_for_automation


def test_extra_watering_rejected_when_soil_already_moist() -> None:
    d = _decide(EXTRA_WATERING, soil_moisture_pct=WET_ENOUGH_PCT + 5)
    assert d.result is PolicyResult.rejected


def test_extra_watering_rejected_when_recently_watered() -> None:
    # Soil is dry enough to water, but it was watered 30 minutes ago.
    d = _decide(EXTRA_WATERING, soil_moisture_pct=40.0, minutes_since_last_watering=30.0)
    assert d.result is PolicyResult.rejected


def test_extra_watering_deferred_when_no_reading() -> None:
    d = _decide(EXTRA_WATERING, soil_moisture_pct=None)
    assert d.result is PolicyResult.scheduled


# --- skip_scheduled_watering ------------------------------------------------


def test_skip_accepted_when_soil_moist_enough() -> None:
    d = _decide(SKIP_WATERING, soil_moisture_pct=70.0)
    assert d.result is PolicyResult.accepted_for_automation


def test_skip_rejected_when_soil_too_dry() -> None:
    # Safety override: the plant needs water, so the skip is refused.
    d = _decide(SKIP_WATERING, soil_moisture_pct=DRY_NEEDS_WATER_PCT - 5)
    assert d.result is PolicyResult.rejected


def test_skip_rejected_when_no_reading_keeps_watering() -> None:
    d = _decide(SKIP_WATERING, soil_moisture_pct=None)
    assert d.result is PolicyResult.rejected


# --- contract guarantees ----------------------------------------------------


def test_unknown_action_is_rejected() -> None:
    d = _decide("request_pruning", soil_moisture_pct=50.0)
    assert d.result is PolicyResult.rejected


@pytest.mark.parametrize(
    ("action_type", "soil"),
    [
        (EXTRA_WATERING, 20.0),
        (EXTRA_WATERING, 80.0),
        (EXTRA_WATERING, None),
        (SKIP_WATERING, 70.0),
        (SKIP_WATERING, 10.0),
        (SKIP_WATERING, None),
        ("something_else", 50.0),
    ],
)
def test_every_decision_has_a_nonempty_reason(action_type: str, soil: float | None) -> None:
    d = _decide(action_type, soil_moisture_pct=soil)
    assert d.reason.strip()
