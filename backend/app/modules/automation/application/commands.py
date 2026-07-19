"""Actuator command creation and idempotency.

An accepted automation decision becomes an ``AutomationCommandV1`` carrying a stable
idempotency key, so a retried request never runs the actuator twice (``AGENTS.md`` §8;
ADR-0005). The requested duration is capped by the watchdog ceiling and turned into an
absolute watchdog deadline.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from app.modules.automation.api.schemas import AutomationCommandV1, CommandSource


def command_idempotency_key(
    source_request_id: str,
    action_type: str,
    request_idempotency_key: str | None = None,
) -> str:
    """Stable idempotency key for a command derived from its request.

    Prefer the client-supplied key; otherwise derive one from the request so a retry of
    the *same* request produces the *same* key (ADR-0005: the key derives from the
    decision, not from the transport attempt).
    """
    return request_idempotency_key or f"{source_request_id}:{action_type}"


def build_watering_command(
    *,
    command_id: str,
    plot_id: str,
    actuator_id: str,
    source_request_id: str,
    action_type: str,
    reason: str,
    requested_duration_seconds: int,
    max_duration_seconds: int,
    issued_at: datetime,
    policy_version: int | None = None,
    request_idempotency_key: str | None = None,
) -> AutomationCommandV1:
    """Build the actuator command for an accepted watering decision.

    The requested duration is capped by the actuator's watchdog ceiling — never trusted
    from the client alone (ADR-0005) — and that ceiling becomes an absolute deadline.
    """
    capped_seconds = max(0, min(requested_duration_seconds, max_duration_seconds))
    return AutomationCommandV1(
        command_id=command_id,
        plot_id=plot_id,
        actuator_id=actuator_id,
        command_type="start_watering",
        source=CommandSource.player_request,
        reason=reason,
        idempotency_key=command_idempotency_key(
            source_request_id, action_type, request_idempotency_key
        ),
        issued_at=issued_at,
        requested_duration_seconds=capped_seconds,
        watchdog_deadline_at=issued_at + timedelta(seconds=capped_seconds),
        policy_version=policy_version,
        source_request_id=source_request_id,
    )


class IdempotencyStore(ABC):
    """Remembers issued commands by idempotency key so a retry does not double-run.

    The in-memory implementation below is process-local, for development and tests. The
    durable store (Weeks 7-8) MUST rely on a UNIQUE constraint on ``idempotency_key``,
    not a read-then-write: two concurrent publishes can both read "absent" and both
    insert (a TOCTOU race), and only the unique constraint closes that window.
    """

    @abstractmethod
    async def get(self, key: str) -> AutomationCommandV1 | None: ...

    @abstractmethod
    async def put(self, key: str, command: AutomationCommandV1) -> None: ...


class InMemoryIdempotencyStore(IdempotencyStore):
    """Process-local idempotency store (development / tests)."""

    def __init__(self) -> None:
        self._by_key: dict[str, AutomationCommandV1] = {}

    async def get(self, key: str) -> AutomationCommandV1 | None:
        return self._by_key.get(key)

    async def put(self, key: str, command: AutomationCommandV1) -> None:
        self._by_key[key] = command


async def issue_command(
    store: IdempotencyStore, command: AutomationCommandV1
) -> tuple[AutomationCommandV1, bool]:
    """Register a command, deduplicating on its idempotency key.

    Returns ``(command, is_new)``. A key already seen returns the *stored* command with
    ``is_new=False``, so a redelivered or retried request never runs the actuator a
    second time (``AGENTS.md`` §8).
    """
    existing = await store.get(command.idempotency_key)
    if existing is not None:
        return existing, False
    await store.put(command.idempotency_key, command)
    return command, True
