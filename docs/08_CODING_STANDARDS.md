# Coding Standards

## General

- Prefer simple, explicit code.
- Keep business rules deterministic and testable.
- Avoid speculative abstractions.
- Reject invalid state transitions explicitly.
- Never use UI state as the source of truth.
- Use English for code and comments.
- Comments explain reasoning, constraints, or safety behavior.
- Use structured logs; do not log secrets or personal data.

## Python

- Use type hints.
- Use async only where it provides real I/O benefit.
- Use Pydantic schemas at boundaries.
- Keep SQLAlchemy models separate from API schemas and domain objects.
- Use Ruff for linting/formatting when tool configuration is added.
- Use Pytest for tests.
- Raise domain-specific exceptions and map them at the API boundary.

Suggested layout:

```text
app/
  modules/
    leases/
      domain/
      application/
      infrastructure/
      api/
      tests/
```

## TypeScript

- Enable strict mode.
- Avoid `any`; document unavoidable exceptions.
- Keep server data in query/cache state and Phaser rendering state in the game adapter.
- Use feature modules.
- Validate external payloads.
- Do not duplicate backend business rules as authoritative frontend rules.

## Database

- All schema changes use migrations.
- Add indexes for measured query needs.
- Use check constraints for stable invariants.
- Avoid soft delete by default; use explicit lifecycle states when history matters.
- Do not edit historical audit or care records in place without a correction record.

## APIs

- Base path: `/api/v1`.
- Use nouns for resources.
- Use explicit commands for domain actions when CRUD is misleading:
  - `POST /leases/{id}/activate`
  - `POST /player-action-requests/{id}/cancel`
  - `POST /work-orders/{id}/complete`
- Use idempotency keys for retried commands.
- Return machine-readable error codes and human-readable messages.
- Document state-transition errors.

## Error codes

Use stable codes such as:

```text
PLOT_NOT_AVAILABLE
LEASE_NOT_ACTIVE
CROP_NOT_ALLOWED
ACTION_REJECTED_BY_POLICY
COMMAND_ACK_TIMEOUT
WORK_ORDER_EVIDENCE_REQUIRED
HARVEST_SAFETY_HOLD
```
