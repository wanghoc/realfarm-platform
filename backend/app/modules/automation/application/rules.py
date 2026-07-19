"""Rule engine v1 — telemetry-driven automation rules.

A rule reads recent telemetry for a plot and, when a condition holds, emits an automation
command. Rule v1: air temperature above a threshold starts ventilation. Commands are
deduplicated by idempotency key, so a rule that keeps firing while the condition holds
does not spam the actuator (``AGENTS.md`` §8; ADR-0005).
"""

import uuid
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Protocol

import structlog

from app.modules.automation.api.schemas import AutomationCommandV1, CommandSource
from app.modules.automation.application.commands import IdempotencyStore, issue_command

log = structlog.get_logger()

SENSOR_AIR_TEMPERATURE = "air_temperature"


class TelemetryReader(Protocol):
    """Reads the latest valid value of a sensor for a plot (persisted telemetry)."""

    async def latest(self, plot_id: str, sensor_type: str) -> float | None: ...


class Rule(ABC):
    """A telemetry condition that, when true, produces one automation command."""

    @abstractmethod
    async def evaluate(self, plot_id: str, reader: TelemetryReader) -> AutomationCommandV1 | None:
        """Return the command to issue when the condition holds, else ``None``."""
        raise NotImplementedError


@dataclass(frozen=True)
class HighTemperatureRuleConfig:
    threshold_celsius: float = 32.0
    fan_duration_seconds: int = 300
    max_duration_seconds: int = 600  # watchdog ceiling for the fan actuator


class HighTemperatureRule(Rule):
    """``air_temperature`` above the threshold starts ventilation for the plot."""

    def __init__(
        self,
        config: HighTemperatureRuleConfig | None = None,
        clock: Callable[[], datetime] = lambda: datetime.now(UTC),
        policy_version: int = 1,
    ) -> None:
        self._cfg = config or HighTemperatureRuleConfig()
        self._clock = clock
        self._policy_version = policy_version

    async def evaluate(self, plot_id: str, reader: TelemetryReader) -> AutomationCommandV1 | None:
        temperature = await reader.latest(plot_id, SENSOR_AIR_TEMPERATURE)
        if temperature is None or temperature <= self._cfg.threshold_celsius:
            return None

        now = self._clock()
        capped = min(self._cfg.fan_duration_seconds, self._cfg.max_duration_seconds)
        return AutomationCommandV1(
            command_id=str(uuid.uuid4()),
            plot_id=plot_id,
            actuator_id=f"fan-{plot_id}",
            command_type="start_ventilation",
            source=CommandSource.automation,
            reason=(
                f"air_temperature {temperature:.1f}C above "
                f"{self._cfg.threshold_celsius:.1f}C threshold."
            ),
            # one command per plot while the condition holds; dedup absorbs re-firing
            idempotency_key=f"{plot_id}:high_temperature",
            issued_at=now,
            requested_duration_seconds=capped,
            watchdog_deadline_at=now + timedelta(seconds=capped),
            policy_version=self._policy_version,
        )


class RuleEngine:
    """Runs rules for a plot and issues the resulting commands, deduplicated."""

    def __init__(self, rules: Iterable[Rule], store: IdempotencyStore) -> None:
        self._rules = list(rules)
        self._store = store

    async def run(self, plot_id: str, reader: TelemetryReader) -> list[AutomationCommandV1]:
        """Evaluate every rule; return only the commands newly issued this run."""
        issued: list[AutomationCommandV1] = []
        for rule in self._rules:
            command = await rule.evaluate(plot_id, reader)
            if command is None:
                continue
            registered, is_new = await issue_command(self._store, command)
            if is_new:
                issued.append(registered)
                log.info(
                    "automation.rule_fired",
                    rule=type(rule).__name__,
                    plot_id=plot_id,
                    command_id=registered.command_id,
                    command_type=registered.command_type,
                    idempotency_key=registered.idempotency_key,
                )
        return issued
