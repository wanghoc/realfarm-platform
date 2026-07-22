# ADR 0006 — Actuator Command Idempotency and Watchdog Enforcement

- Status: Proposed

## Context

A player action can become an automation command (ADR-0003;
`docs/15_ACTION_CATALOG.md` Category A). A command drives a real actuator — a pump, a
valve, a fan, a grow light — so two failure modes are physical, not cosmetic:

- **Double execution.** MQTT delivery is at-least-once (QoS 1, see the simulator/gateway
  contract). A redelivered or retried command must not run a pump a second time.
- **A device outliving its command.** `AGENTS.md` §8 requires watchdog limits for
  actuators and forbids reporting a failed acknowledgement as a completed action. A pump
  that keeps running after the backend loses contact is the hazard this guards against.

This ADR fixes the command schema and the enforcement model now (Week 4), so the runtime
built in Weeks 7-8 (`docs/10_ROADMAP_16_WEEKS.md`) has a stable target. It does not build
the runtime.

## Decision

**Idempotency.** Every command in `packages/contracts/schemas/automation-command.v1.json`
carries a required `idempotencyKey`. The key is derived from the authorized decision, not
from the transport attempt, so retrying the same decision produces the same key. Both the
publisher and the gateway deduplicate on it: a key already seen MUST NOT run the actuator
again.

**Watchdog.** Every command may carry an absolute `watchdogDeadlineAt`, bounded by the
actuator's server-side maximum duration ceiling — never by the client's requested duration
alone. Enforcement is two-layer:

1. the gateway stops the actuator locally at the deadline even if the backend is
   unreachable;
2. a durable backend job (`docs/03_ARCHITECTURE.md`, "Durable asynchronous work") stops it
   and records `stopped_by_watchdog` if no final acknowledgement arrives by the deadline.

The deadline is an absolute timestamp rather than a relative duration precisely so it
survives a process restart and can be enforced by a durable job.

The interfaces that encode this decision ship in this change: `AutomationCommandV1`
(`automation/api/schemas.py`), the `Watchdog` interface (`automation/application/watchdog.py`),
and the `ActionPolicyEngine` interface (`player_actions/application/policy.py`).

## Alternatives considered

- **Idempotency by a `(plot, actuator, timestamp)` tuple** instead of an explicit key —
  rejected: timestamps skew and collide, and the tuple is not stable across a retry. An
  explicit unique key is unambiguous and auditable.
- **Watchdog enforced only in the backend** — rejected: a network partition would let an
  actuator run unbounded until the connection returns. The edge must be able to stop on its
  own.
- **Watchdog enforced only at the edge** — rejected: an edge that crashes mid-run leaves no
  authoritative record. The durable backend job is both the backstop and the audit trail.
- **A relative `runForSeconds` timed locally by the gateway, as the sole mechanism** —
  rejected: a backend restart loses the in-flight timer. An absolute deadline is
  reconstructable; the relative duration is kept only as `requestedDurationSeconds` for
  intent-vs-actual comparison.

## Consequences

- `automation-command.v1` requires `idempotencyKey` and carries an optional
  `watchdogDeadlineAt` (required in practice for any timed actuator run).
- The gateway MUST persist seen idempotency keys and the active deadline across reconnects.
- Commands stay reconstructable per ADR-0003: `source`, `policyVersion`, and a
  human-readable `reason` are on every command.
- The durable watchdog job and the per-actuator ceilings are implemented in Weeks 7-8; this
  ADR only fixes the contract and interfaces.

## Follow-up

- Default watchdog ceiling per actuator type (pump / valve / fan / grow light) — needs a
  hardware/agronomy value; decided with the Weeks 7-8 telemetry slice.
- Idempotency-key retention window on the gateway (how long a key is remembered) versus its
  storage cost.
- Whether `request_camera_snapshot` flows through this command path or the `media` module
  directly (mirrors the open question in `docs/15_ACTION_CATALOG.md` §7).
