# ERD — Telemetry, Automation, Work Orders

> Week 2 deliverable for issue #7 (`role:khoa`). Entity-relationship design for the
> `telemetry`, `automation`, and `work_orders` modules. This is a **conceptual** ERD:
> the final SQL schema must be created through Alembic migrations
> (`docs/07_DATA_MODEL_GUIDE.md`).
>
> Read alongside: `docs/02_BUSINESS_RULES.md`, `docs/04_DOMAIN_MODEL.md`,
> `docs/07_DATA_MODEL_GUIDE.md` (authoritative table list),
> `docs/15_ACTION_CATALOG.md`, `docs/16_OPERATOR_WORKFLOW.md`,
> `docs/adr/0003-policy-controlled-player-actions.md`, and the contracts in
> `packages/contracts/schemas/`.

Normative keywords `MUST`, `SHOULD`, and `MAY` follow `docs/02_BUSINESS_RULES.md`.

## 1. Scope

This ERD covers the tables owned by the three modules in scope, as named in
`docs/07_DATA_MODEL_GUIDE.md`:

| Module | Tables |
|---|---|
| `telemetry` | `devices`, `sensors`, `actuators`, `measurements` |
| `automation` | `action_policies`, `automation_commands` |
| `work_orders` | `work_orders`, `work_order_items`, `work_evidence` |

Tables owned by other modules (`plots`, `crop_cycles`, `users`,
`player_action_requests`, `care_logs`) appear only as relationship endpoints. No table
outside the list in `07_DATA_MODEL_GUIDE.md` is introduced.

## 2. Diagram

```mermaid
erDiagram
    plots ||--o{ devices : "hosts"
    plots ||--o{ sensors : "monitored by"
    plots ||--o{ actuators : "actuated by"
    devices ||--o{ sensors : "exposes"
    devices ||--o{ actuators : "exposes"
    sensors ||--o{ measurements : "produces"
    actuators ||--o{ automation_commands : "targets"
    action_policies ||--o{ automation_commands : "authorized by"
    player_action_requests ||--o{ automation_commands : "may originate"
    player_action_requests ||--o{ work_order_items : "may originate"
    work_orders ||--|{ work_order_items : "groups"
    work_order_items ||--o{ work_evidence : "evidenced by"
    work_order_items ||--o{ care_logs : "records"
    plots ||--o{ work_order_items : "scoped to"
    crop_cycles ||--o{ work_order_items : "scoped to"
    users ||--o{ work_orders : "assigned to"

    devices {
        uuid id PK
        string public_id UK "opaque, exposed externally"
        uuid farm_id FK
        uuid plot_id FK "nullable: farm-level devices"
        string device_type "gateway|sensor_node|actuator_node|camera"
        string hardware_id UK "vendor identity"
        string status "active|offline|maintenance|retired"
        timestamptz last_seen_at "nullable"
        timestamptz created_at
        timestamptz updated_at
    }

    sensors {
        uuid id PK
        uuid device_id FK
        uuid plot_id FK "nullable"
        string sensor_type "air_temperature|air_humidity|soil_moisture|light|ph"
        string unit "MUST match sensor_type"
        string status "active|faulty|retired"
        timestamptz calibrated_at "nullable"
        timestamptz created_at
    }

    actuators {
        uuid id PK
        uuid device_id FK
        uuid plot_id FK
        string actuator_type "pump|valve|fan|grow_light"
        string status "active|faulty|retired"
        int max_duration_seconds "watchdog ceiling"
        int min_interval_seconds "anti-thrash guard"
        timestamptz created_at
    }

    measurements {
        timestamptz measured_at PK "hypertable time column"
        uuid sensor_id PK, FK
        string message_id UK "dedupe key from iot-measurement.v1"
        uuid device_id FK
        uuid plot_id FK "denormalized for query speed"
        string sensor_type
        numeric value
        string unit
        string quality "valid|suspect|invalid"
        string quarantine_reason "nullable, required when quality != valid"
        string signature "nullable, integrity proof"
        timestamptz ingested_at
    }

    action_policies {
        uuid id PK
        string action_type "see docs/15_ACTION_CATALOG.md"
        int version "bumped, never edited in place"
        jsonb rules
        timestamptz effective_from
        timestamptz effective_to "nullable"
        uuid created_by FK
        timestamptz created_at
    }

    automation_commands {
        uuid id PK
        string public_id UK
        uuid actuator_id FK
        uuid plot_id FK
        string command_type
        jsonb parameters
        string source "automation|operator|player_request|emergency"
        uuid source_request_id FK "nullable, player_action_requests"
        uuid policy_id FK "nullable, policy that authorized it"
        int policy_version
        string reason "human-readable, always present"
        string idempotency_key UK
        int requested_duration_seconds "nullable"
        int actual_duration_seconds "nullable, set on final state"
        timestamptz watchdog_deadline_at "nullable"
        string status "created|published|acknowledged|running|succeeded|rejected_by_gateway|timed_out|failed|stopped_by_watchdog|cancelled"
        timestamptz published_at "nullable"
        timestamptz acknowledged_at "nullable"
        timestamptz completed_at "nullable"
        uuid created_by FK "nullable for system actor"
        timestamptz created_at
    }

    work_orders {
        uuid id PK
        string public_id UK
        uuid farm_id FK
        string status "draft|assigned|accepted|in_progress|completed|verified|blocked|cancelled (see 4.1)"
        string priority "low|normal|high|urgent"
        uuid assignee_id FK "nullable until assigned"
        timestamptz due_from "nullable"
        timestamptz due_to "nullable"
        string status_reason "nullable, required for blocked|cancelled|rejected"
        int version "optimistic locking"
        uuid created_by FK "nullable for system-drafted"
        timestamptz created_at
        timestamptz updated_at
    }

    work_order_items {
        uuid id PK
        uuid work_order_id FK
        uuid plot_id FK "exactly one"
        uuid crop_cycle_id FK "exactly one"
        string task_type "pest_inspection|general_inspection|nutrient_check|manual_watering|pruning|treatment"
        uuid source_request_id FK "nullable, player_action_requests"
        string evidence_exception_reason "nullable"
        uuid evidence_exception_approved_by FK "nullable, reviewer"
        timestamptz evidence_exception_approved_at "nullable"
        timestamptz created_at
    }

    work_evidence {
        uuid id PK
        uuid work_order_item_id FK
        string kind "before|after"
        string media_type "image|video|note"
        string storage_key
        string content_hash "integrity, may be anchored per ADR-0004"
        timestamptz captured_at
        uuid captured_by FK
        timestamptz created_at
    }
```

## 3. Telemetry

### 3.1 Device / sensor / actuator split

`devices` is the physical unit that talks MQTT; `sensors` and `actuators` are the
capabilities it exposes. The split matches `07_DATA_MODEL_GUIDE.md` and keeps a single
gateway able to serve several plots.

Watchdog ceilings live on `actuators` (`max_duration_seconds`), not in application
code, so the limit survives a restart and is auditable (`AGENTS.md` §8).

### 3.2 Measurements

`measurements` is the TimescaleDB hypertable, partitioned on `measured_at`. It stores
**one row per measurement**, matching `packages/contracts/schemas/iot-measurement.v1.json`
(one `sensorType` + `value` + `unit` per message), not a batched array.

- Every row MUST carry timestamp, device identity, unit, and quality (`AGENTS.md` §8).
- `message_id` is unique and makes ingest idempotent: a redelivered MQTT message MUST
  NOT create a second row.
- `unit` MUST match `sensor_type` (`07_DATA_MODEL_GUIDE.md`). Enforce in the ingest
  use case and with a check constraint where practical.
- `plot_id` is denormalized from `sensors` because nearly every read is "latest by
  plot" (`telemetry/api/router.py`).

### 3.3 Quarantine

Suspicious or invalid readings MUST NOT be silently treated as valid (`AGENTS.md` §8).
This ERD keeps them **in the same hypertable**, marked by `quality` and explained by
`quarantine_reason`, rather than moving them to a separate table:

- the raw value stays available for AI training and incident forensics;
- `07_DATA_MODEL_GUIDE.md` lists no quarantine table, and this ERD does not invent one.

Every read path that feeds policy decisions, player-facing UI, or automation MUST
filter `quality = 'valid'`. A quarantined row is evidence, not a measurement.

## 4. Work orders

### 4.1 Contract drift — `rejected` is missing from the contract

**This needs a decision from Học before the `work_orders` migration is written**
(Weeks 9-10, "Human work orchestration", `docs/10_ROADMAP_16_WEEKS.md`).

`docs/04_DOMAIN_MODEL.md` lists the WorkOrder alternative states as `rejected`,
`cancelled`, `blocked`. `docs/16_OPERATOR_WORKFLOW.md` documents the transition
`assigned → rejected` (an operator declines an assignment, freeing it for reassignment).

But `packages/contracts/schemas/work-order.v1.json` `status` enum is:

```text
draft | assigned | accepted | in_progress | completed | verified | blocked | cancelled
```

`rejected` is **absent**. The contract and the domain model contradict each other, so
the `status` column above cannot be finalized yet. Options:

1. **Add `rejected` to the contract** — matches `04_DOMAIN_MODEL.md` and the operator
   workflow; requires a `work-order.v1` change (a widened enum is backward-compatible
   for readers, but consumers must handle the new value).
2. **Drop `rejected` from the domain model** — model a declined assignment as
   `assigned → draft` plus a `status_reason`, keeping the contract untouched.

This ERD does not pick a side. Until it is resolved, `work_orders.status` follows the
**contract** (the narrower set), and the drift is tracked in
`docs/13_ASSUMPTIONS_AND_OPEN_QUESTIONS.md` and §6 below.

### 4.2 Order / item split

A work order groups items; each item is bound to **exactly one** `plot_id` and one
`crop_cycle_id` (`07_DATA_MODEL_GUIDE.md`). This is what makes batching safe: one
operator visit can serve many plots while per-plot traceability survives
(`docs/16_OPERATOR_WORKFLOW.md` §7).

`source_request_id` links an item back to the player request that caused it, so a
player can be shown the outcome of their own request.

### 4.3 Evidence

Completion SHOULD include before/after evidence (`docs/02_BUSINESS_RULES.md`). The
evidence exception lives on `work_order_items` — reason, approving reviewer, and
approval time — so a `complete` without evidence is either blocked by
`WORK_ORDER_EVIDENCE_REQUIRED` (`docs/08_CODING_STANDARDS.md`) or carries an explicit,
attributable approval. `content_hash` supports the optional integrity anchoring in
ADR-0004 without putting media on-chain.

## 5. Automation

`automation_commands` records everything ADR-0003 and `AGENTS.md` §8 require to answer
"who caused this actuator to run, under which policy, and what actually happened":

- `source` distinguishes `automation` / `operator` / `player_request` / `emergency`;
- `source_request_id` + `policy_id` + `policy_version` reconstruct the decision, which
  is why `action_policies` is versioned and append-only rather than edited in place;
- `idempotency_key` is unique, so a retried publish cannot double-run a pump;
- `watchdog_deadline_at` makes `stopped_by_watchdog` enforceable by a durable job even
  if the requesting process died;
- `requested_duration_seconds` vs `actual_duration_seconds` exposes the gap between
  intent and reality, which is what `care_logs` and incident review need.

Emergency automation MAY create commands that contradict a player preference
(`AGENTS.md` §2); `source = 'emergency'` and `reason` record why.

## 6. Open questions (for cross-review with Học)

Tracked against `docs/13_ASSUMPTIONS_AND_OPEN_QUESTIONS.md`:

1. **`rejected` in `work-order.v1` (§4.1)** — widen the contract, or drop the state from
   the domain model? Blocks the `work_orders` migration (Weeks 9-10).
2. Quarantined rows in `measurements` vs a separate table (§3.3) — does the AI/infra
   side (Bảo) need them in one hypertable for training, or filtered out at ingest?
3. `measurements` retention and continuous-aggregate policy — how long is raw telemetry
   kept before rollup? Affects hypertable chunk sizing.
4. Do `sensors`/`actuators` need farm-level rows (`plot_id` null), or is every device
   plot-bound in the MVP?
5. Is `care_logs` written by the `work_orders` module on item completion, or by
   `care_logs` itself listening for an event? Ownership boundary with Học.
6. Opaque `public_id` — one shared generator, or per-table? (`07_DATA_MODEL_GUIDE.md`
   requires opaque public identifiers.)
