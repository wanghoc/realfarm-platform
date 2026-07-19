"""Concrete deadline watchdog (Watchdog v1).

Stops an actuator command once its absolute watchdog deadline passes without a final
acknowledgement (``AGENTS.md`` §8; ADR-0005). The deadline is absolute so the sweep can
run from a durable job and survive a restart; durable scheduling itself lands with the
Weeks 7-8 persistence — this is the enforcement logic that job calls.
"""

import uuid
from collections.abc import Iterable
from datetime import UTC, datetime, timedelta

import structlog

from app.modules.automation.api.schemas import AutomationCommandV1, CommandSource
from app.modules.automation.application.watchdog import Watchdog

log = structlog.get_logger()


class DeadlineWatchdog(Watchdog):
    """Enforces the actuator's watchdog ceiling as an absolute deadline."""

    def deadline_for(self, command: AutomationCommandV1, max_duration_seconds: int) -> datetime:
        requested = command.requested_duration_seconds or 0
        capped = max(0, min(requested, max_duration_seconds))
        return command.issued_at + timedelta(seconds=capped)

    def is_expired(self, deadline: datetime, now: datetime) -> bool:
        return now > deadline

    async def on_deadline_exceeded(self, command: AutomationCommandV1) -> AutomationCommandV1:
        """Emit the stop command for an expired actuator command, and log it.

        Refines the base signature (which returns ``None``): returning the stop command
        lets the caller publish it. Its idempotency key is derived from the original so a
        repeated sweep does not enqueue two stops.
        """
        now = datetime.now(UTC)
        stop = AutomationCommandV1(
            command_id=str(uuid.uuid4()),
            plot_id=command.plot_id,
            actuator_id=command.actuator_id,
            command_type="stop",
            source=CommandSource.emergency,
            reason=f"Watchdog: command {command.command_id} exceeded its safe deadline.",
            idempotency_key=f"watchdog-stop:{command.idempotency_key}",
            issued_at=now,
        )
        log.warning(
            "automation.watchdog_stopped",
            stopped_command_id=command.command_id,
            plot_id=command.plot_id,
            actuator_id=command.actuator_id,
            stop_command_id=stop.command_id,
        )
        return stop


async def sweep(
    watchdog: DeadlineWatchdog,
    commands: Iterable[AutomationCommandV1],
    now: datetime,
    max_duration_seconds: int,
) -> list[AutomationCommandV1]:
    """Return a stop command for every command whose watchdog deadline has passed."""
    stops: list[AutomationCommandV1] = []
    for command in commands:
        deadline = command.watchdog_deadline_at or watchdog.deadline_for(
            command, max_duration_seconds
        )
        if watchdog.is_expired(deadline, now):
            stops.append(await watchdog.on_deadline_exceeded(command))
    return stops
