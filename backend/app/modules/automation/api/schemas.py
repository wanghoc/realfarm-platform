"""Automation command contract (code mirror).

``AutomationCommandV1`` mirrors ``packages/contracts/schemas/automation-command.v1.json``
— the validated command the backend publishes to the gateway/simulator on
``realfarm/plots/{plot_id}/commands``. Every command carries an idempotency key so a
retried publish never double-runs an actuator, and a watchdog deadline so a device
cannot outlive its command (``AGENTS.md`` §8). Design rationale: ADR-0005.
"""

from datetime import datetime
from enum import StrEnum

from app.core.schema import CamelModel


class CommandSource(StrEnum):
    """Who caused the command (``AGENTS.md`` §8; ``docs/15_ACTION_CATALOG.md``)."""

    automation = "automation"
    operator = "operator"
    player_request = "player_request"
    emergency = "emergency"


class AutomationCommandV1(CamelModel):
    """One actuator command, matching ``realfarm.automation-command.v1``."""

    command_id: str
    plot_id: str
    actuator_id: str
    command_type: str
    source: CommandSource
    reason: str
    idempotency_key: str
    issued_at: datetime
    parameters: dict | None = None
    requested_duration_seconds: int | None = None
    watchdog_deadline_at: datetime | None = None
    policy_version: int | None = None
    source_request_id: str | None = None
