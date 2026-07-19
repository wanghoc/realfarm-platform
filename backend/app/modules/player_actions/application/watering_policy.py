"""Watering action policy — the first concrete ActionPolicyEngine.

Implements the policy for the two sample watering actions from
``docs/15_ACTION_CATALOG.md`` (Category A): ``request_extra_watering`` and
``skip_scheduled_watering``. This is the "start the real policy engine" step (issue #23).
The sensor / quota / window inputs a full engine reads land with the telemetry slice in
Weeks 7-8, so soil-moisture signals arrive here through an injected provider that is
stubbed today — the policy logic is complete and testable without persisted telemetry.
"""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol

from app.modules.player_actions.api.schemas import (
    PlayerActionRequestV1,
    PolicyDecision,
    PolicyOutcome,
)
from app.modules.player_actions.application.policy import ActionPolicyEngine

ACTION_EXTRA_WATERING = "request_extra_watering"
ACTION_SKIP_WATERING = "skip_scheduled_watering"


@dataclass(frozen=True)
class WateringSignals:
    """The plot signals the watering policy needs in order to decide safely."""

    soil_moisture_percent: float
    seconds_since_last_watering: float | None  # None when never watered / unknown


class WateringSignalsProvider(Protocol):
    """Supplies current watering signals for a plot.

    Stubbed for issue #23; the real provider reads persisted telemetry (Weeks 7-8).
    """

    async def get(self, plot_id: str) -> WateringSignals: ...


@dataclass(frozen=True)
class WateringPolicyConfig:
    """Thresholds for the watering policy. Versioned so a decision is reconstructable."""

    version: int = 1
    request_ttl_seconds: int = 300
    # extra watering is unnecessary (so rejected) at or above this soil moisture
    moist_threshold_percent: float = 60.0
    # ... or when the plot was watered more recently than this
    min_reirrigation_interval_seconds: int = 3600
    # skipping watering is unsafe (so rejected) below this soil moisture
    critical_moisture_percent: float = 25.0


class WateringPolicyEngine(ActionPolicyEngine):
    """Evaluates watering requests into a policy decision.

    Safety overrides preference (``AGENTS.md`` §2): ``skip_scheduled_watering`` is
    rejected when the soil is critically dry, even though the player asked to skip.
    """

    def __init__(
        self,
        signals: WateringSignalsProvider,
        config: WateringPolicyConfig | None = None,
        clock: Callable[[], datetime] = lambda: datetime.now(UTC),
    ) -> None:
        self._signals = signals
        self._config = config or WateringPolicyConfig()
        self._clock = clock

    async def evaluate(self, request: PlayerActionRequestV1) -> PolicyDecision:
        cfg = self._config

        age_seconds = (self._clock() - request.requested_at).total_seconds()
        if age_seconds > cfg.request_ttl_seconds:
            return self._decide(
                PolicyOutcome.expired,
                f"Request older than the {cfg.request_ttl_seconds}s TTL.",
            )

        if request.action_type == ACTION_EXTRA_WATERING:
            return await self._evaluate_extra_watering(request)
        if request.action_type == ACTION_SKIP_WATERING:
            return await self._evaluate_skip_watering(request)
        return self._decide(
            PolicyOutcome.rejected,
            f"Unsupported action_type '{request.action_type}' for the watering policy.",
        )

    async def _evaluate_extra_watering(self, request: PlayerActionRequestV1) -> PolicyDecision:
        cfg = self._config
        signals = await self._signals.get(request.plot_id)
        if signals.soil_moisture_percent >= cfg.moist_threshold_percent:
            return self._decide(
                PolicyOutcome.rejected,
                f"Soil already moist ({signals.soil_moisture_percent:.0f}% >= "
                f"{cfg.moist_threshold_percent:.0f}%); extra watering not needed.",
            )
        if (
            signals.seconds_since_last_watering is not None
            and signals.seconds_since_last_watering < cfg.min_reirrigation_interval_seconds
        ):
            return self._decide(
                PolicyOutcome.rejected,
                "Plot was watered too recently; wait before adding more.",
            )
        return self._decide(
            PolicyOutcome.accepted_for_automation,
            "Soil below target and no recent watering; safe to add watering.",
        )

    async def _evaluate_skip_watering(self, request: PlayerActionRequestV1) -> PolicyDecision:
        cfg = self._config
        signals = await self._signals.get(request.plot_id)
        if signals.soil_moisture_percent < cfg.critical_moisture_percent:
            return self._decide(
                PolicyOutcome.rejected,
                f"Soil critically dry ({signals.soil_moisture_percent:.0f}% < "
                f"{cfg.critical_moisture_percent:.0f}%); safety requires watering, cannot skip.",
            )
        return self._decide(
            PolicyOutcome.accepted_for_automation,
            "Soil sufficient; the scheduled watering may be skipped.",
        )

    def _decide(self, outcome: PolicyOutcome, reason: str) -> PolicyDecision:
        return PolicyDecision(result=outcome, reason=reason, policy_version=self._config.version)
