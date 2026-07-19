"""Actuator watchdog interface.

An actuator command carries a hard time limit so a device cannot outlive its command
(``AGENTS.md`` §8: "Add watchdog limits for actuators"). This module defines only the
interface; the durable enforcement job and the per-actuator ceilings land in Weeks 7-8
(``docs/10_ROADMAP_16_WEEKS.md``). Design rationale: ADR-0005.
"""

from abc import ABC, abstractmethod
from datetime import datetime

from app.modules.automation.api.schemas import AutomationCommandV1


class Watchdog(ABC):
    """Computes and enforces the deadline past which an actuator MUST be stopped.

    Two layers enforce the same ceiling (ADR-0005):

    - the gateway stops the actuator locally even if the backend is unreachable;
    - a durable backend job stops it and records ``stopped_by_watchdog`` if no final
      acknowledgement arrives by the deadline — which is why the deadline is an absolute
      timestamp, so it survives a process restart.
    """

    @abstractmethod
    def deadline_for(self, command: AutomationCommandV1, max_duration_seconds: int) -> datetime:
        """Absolute time by which the command must complete or be stopped.

        Bounded by the actuator's ``max_duration_seconds`` ceiling, never by the
        client's requested duration alone.
        """
        raise NotImplementedError

    @abstractmethod
    def is_expired(self, deadline: datetime, now: datetime) -> bool:
        """True when ``now`` is past ``deadline`` and no final state was reported."""
        raise NotImplementedError

    @abstractmethod
    async def on_deadline_exceeded(self, command: AutomationCommandV1) -> None:
        """Stop the actuator and mark the command ``stopped_by_watchdog``. Weeks 7-8."""
        raise NotImplementedError
