# Shared Contracts

Versioned contracts shared by API, gateway, simulator, AI service, and web application.

Rules:

- additive compatible changes may keep the version;
- breaking changes require a new schema version;
- producers and consumers must validate payloads;
- contracts are reviewed like code;
- do not place business logic in schemas.

## Layout

```text
packages/contracts/
  schemas/    JSON Schema (Draft 2020-12), one file per contract version
  examples/   sample payloads: <name>.valid.json (must pass), <name>.invalid.json (must fail)
  validate.py test skeleton run by CI and locally
```

## Schemas

| Schema | Produced by | Consumed by | Notes |
|---|---|---|---|
| `iot-measurement.v1` | gateway, simulator | `telemetry` ingest | one reading per message; `messageId` is the dedupe key |
| `player-action-request.v1` | web app | `player_actions` policy engine | `actionType` enum = `docs/15_ACTION_CATALOG.md`; `parameters` free for now |
| `work-order.v1` | `work_orders` | operator app, `work_orders` | see open question below on `status` |
| `harvest-record.v1` | `harvests` | web app, traceability | field set to be cross-reviewed with Học's lease/harvest ERD (#6) |

Every schema sets `additionalProperties: false`. Adding a field is therefore a change
consumers must adopt; follow the versioning rules above.

Cross-field and business rules (e.g. `unit` must match `sensorType`,
`acceptedWeightKg + rejectedWeightKg <= totalWeightKg`) are **not** encoded in the
schemas — they are enforced by the owning module at write time, per "do not place
business logic in schemas."

## Open questions

- **`work-order.v1.status` drift.** `docs/04_DOMAIN_MODEL.md` and
  `docs/16_OPERATOR_WORKFLOW.md` use a `rejected` state (operator declines an
  assignment) that is **absent** from this contract's `status` enum
  (`docs/17_ERD_TELEMETRY_AUTOMATION_WORK_ORDERS.md` §4.1,
  `docs/13_ASSUMPTIONS_AND_OPEN_QUESTIONS.md`). The contract keeps the narrower set
  until Học decides whether to widen the enum or drop the domain state. The
  `work-order.v1.invalid.json` example uses `status: "rejected"` on purpose, so this CI
  fails the day someone relies on the missing value.

## Validating locally

```bash
pip install -r packages/contracts/requirements.txt
python packages/contracts/validate.py
```

`validate.py` checks that every schema is a valid JSON Schema (meta-schema) and that
each `examples/*.valid.json` passes while each `examples/*.invalid.json` is rejected.
The same script runs in `.github/workflows/ci-contracts.yml` on any change under
`packages/contracts/`.
