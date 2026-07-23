"""Watering policy engine (issue #124).

The first *real* ``ActionPolicyEngine`` (not just the #107 interface). It decides the two
Category-A watering actions from ``docs/15_ACTION_CATALOG.md`` §4.1:

- ``request_extra_watering`` — grant only when the soil actually needs water and was not
  just watered; otherwise reject (over-watering is a real hazard) or defer.
- ``skip_scheduled_watering`` — grant only when the soil is not too dry; if the plant
  needs water the skip is rejected, because safety automation overrides player preference
  (``docs/15`` §4.1, ``AGENTS.md`` §2).

Inputs are soil moisture and time since the last watering. Persisted telemetry does not
exist yet, so the engine reads them through a ``PlotConditionProvider`` port; a static
stub stands in for now (the issue explicitly allows stubbed input as long as the policy
logic is correct). The telemetry-backed provider and per-crop thresholds land with the
telemetry slice in Weeks 7-8 (``docs/10_ROADMAP_16_WEEKS.md``).
"""

from dataclasses import dataclass
from typing import Protocol

from app.modules.player_actions.application.policy import (
    ActionPolicyEngine,
    ActionRequest,
    PolicyDecision,
    PolicyResult,
)

# The two Category-A watering actions this engine owns (docs/15 §4.1).
EXTRA_WATERING = "request_extra_watering"
SKIP_WATERING = "skip_scheduled_watering"

# Soil moisture is volumetric water content in percent. These are provisional scaffold
# thresholds; real per-crop values arrive with the telemetry slice in Weeks 7-8.
WET_ENOUGH_PCT = 60.0  # at/above this the soil is already moist — no extra water
DRY_NEEDS_WATER_PCT = 30.0  # below this the plant needs water — a skip is unsafe
RECENT_WATERING_MINUTES = 180.0  # watered within this window → extra watering is redundant


@dataclass(frozen=True)
class PlotConditions:
    """Sensor-derived inputs the watering policy needs for one plot.

    ``None`` means no recent reading is available (e.g. sensor offline), which the policy
    treats conservatively rather than guessing.
    """

    soil_moisture_pct: float | None
    minutes_since_last_watering: float | None


class PlotConditionProvider(Protocol):
    """Supplies current conditions for a plot.

    Backed by persisted telemetry in Weeks 7-8; a static stub implements it until then.
    """

    async def conditions_for(self, plot_id: str) -> PlotConditions: ...


class StaticPlotConditionProvider:
    """Stub provider returning fixed conditions — for scaffolding and tests.

    Real evaluation reads the latest ``soil_moisture`` measurement (see
    ``telemetry`` module) and the last irrigation command; this stand-in lets the policy
    logic ship and be tested before that persistence exists.
    """

    def __init__(self, conditions: PlotConditions) -> None:
        self._conditions = conditions

    async def conditions_for(self, plot_id: str) -> PlotConditions:
        return self._conditions


class WateringPolicyEngine(ActionPolicyEngine):
    """Evaluates the two watering actions against current soil conditions."""

    def __init__(self, conditions: PlotConditionProvider) -> None:
        self._conditions = conditions

    async def evaluate(self, request: ActionRequest) -> PolicyDecision:
        if request.action_type == EXTRA_WATERING:
            conditions = await self._conditions.conditions_for(request.plot_id)
            return self._decide_extra_watering(conditions)
        if request.action_type == SKIP_WATERING:
            conditions = await self._conditions.conditions_for(request.plot_id)
            return self._decide_skip_watering(conditions)
        return PolicyDecision(
            result=PolicyResult.rejected,
            reason=f"{request.action_type!r} is not a watering action.",
        )

    def _decide_extra_watering(self, c: PlotConditions) -> PolicyDecision:
        """Grant extra watering only when the soil needs it and was not just watered."""
        if c.soil_moisture_pct is None:
            return PolicyDecision(
                result=PolicyResult.scheduled,
                reason="No recent soil-moisture reading; deferred until one is available.",
            )
        if c.soil_moisture_pct >= WET_ENOUGH_PCT:
            return PolicyDecision(
                result=PolicyResult.rejected,
                reason=(
                    f"Soil already moist at {c.soil_moisture_pct:.0f}% "
                    f"(>= {WET_ENOUGH_PCT:.0f}% threshold); extra watering not needed."
                ),
            )
        if (
            c.minutes_since_last_watering is not None
            and c.minutes_since_last_watering < RECENT_WATERING_MINUTES
        ):
            return PolicyDecision(
                result=PolicyResult.rejected,
                reason=(
                    f"Watered {c.minutes_since_last_watering:.0f} min ago "
                    f"(within {RECENT_WATERING_MINUTES:.0f} min); extra watering redundant."
                ),
            )
        return PolicyDecision(
            result=PolicyResult.accepted_for_automation,
            reason=(
                f"Soil at {c.soil_moisture_pct:.0f}% is below the {WET_ENOUGH_PCT:.0f}% "
                "moist threshold; safe to add water."
            ),
        )

    def _decide_skip_watering(self, c: PlotConditions) -> PolicyDecision:
        """Grant a skip only when the soil is not too dry; safety overrides preference."""
        if c.soil_moisture_pct is None:
            return PolicyDecision(
                result=PolicyResult.rejected,
                reason=(
                    "No recent soil-moisture reading; keeping the scheduled watering "
                    "as the safe default."
                ),
            )
        if c.soil_moisture_pct < DRY_NEEDS_WATER_PCT:
            return PolicyDecision(
                result=PolicyResult.rejected,
                reason=(
                    f"Soil at {c.soil_moisture_pct:.0f}% is below the "
                    f"{DRY_NEEDS_WATER_PCT:.0f}% minimum; watering must proceed "
                    "(safety overrides preference)."
                ),
            )
        return PolicyDecision(
            result=PolicyResult.accepted_for_automation,
            reason=(
                f"Soil at {c.soil_moisture_pct:.0f}% is adequate; skipping the next "
                "watering is safe."
            ),
        )
