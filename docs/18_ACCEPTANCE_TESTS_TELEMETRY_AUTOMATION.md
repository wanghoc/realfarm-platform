# Acceptance Tests — Telemetry and Automation

> Week 2 deliverable for issue #7 (`role:khoa`). Acceptance criteria for the `telemetry`
> and `automation` modules, written from the IoT/policy point of view.
>
> Read alongside: `docs/09_VALIDATION_STRATEGY.md`, `docs/02_BUSINESS_RULES.md`,
> `docs/15_ACTION_CATALOG.md`, `docs/17_ERD_TELEMETRY_AUTOMATION_WORK_ORDERS.md`,
> `docs/adr/0003-policy-controlled-player-actions.md`, and `AGENTS.md` §8.

## 1. What this document is

`docs/09_VALIDATION_STRATEGY.md` states that **this repository does not keep a dedicated
committed automated test tree**. So this document specifies acceptance criteria in
Given/When/Then form — the observable behavior a change must produce — rather than
committing `pytest` files. Each scenario names how it is checked today.

The behavior is specified now so that the Weeks 7-8 implementation (telemetry
persistence, policy engine, irrigation command, watchdog — `docs/10_ROADMAP_16_WEEKS.md`)
has a target to hit rather than being judged after the fact.

**None of these scenarios pass today.** Both modules are scaffolds:
`telemetry/api/router.py` returns `{"measurements": []}` and `automation/api/router.py`
returns `[]`. Several scenarios are additionally blocked by the simulator payload drift
recorded in `backend/services/simulator/README.md`. Blockers are marked per scenario.

Normative keywords `MUST`, `SHOULD`, and `MAY` follow `docs/02_BUSINESS_RULES.md`.

## 2. How to run these checks

Per `docs/09_VALIDATION_STRATEGY.md`:

```bash
docker compose up -d db mqtt backend simulator
docker compose exec mqtt mosquitto_sub -t 'realfarm/#' -v    # observe telemetry + acks
```

Publish a crafted message to drive a specific scenario:

```bash
docker compose exec mqtt mosquitto_pub \
  -t 'realfarm/plots/plot-001/telemetry' -q 1 -m '<payload>'
```

The development demo account is `demo@realfarm.dev` / `demo1234`.

## 3. Telemetry ingest

### T-01 — A valid measurement is stored and served

- **Given** an active sensor bound to `plot-001`,
- **When** the gateway or simulator publishes a measurement to
  `realfarm/plots/plot-001/telemetry` that satisfies `iot-measurement.v1`,
- **Then** it is persisted with `quality = 'valid'`,
- **And** `GET /api/v1/telemetry/plots/plot-001/latest` returns it with timestamp,
  device identity, unit, and quality status (`AGENTS.md` §8).

*Blocked by:* simulator payload drift; telemetry persistence not implemented.

### T-02 — A replayed message does not duplicate

- **Given** a measurement with `messageId` `m-1` has been ingested,
- **When** the same `messageId` arrives again (MQTT QoS 1 redelivery, or a gateway
  replaying its offline buffer),
- **Then** no second row is created,
- **And** ingest still reports success — a duplicate is expected, not an error.

*Rationale:* `measurements.message_id` is unique
(`docs/17_ERD_TELEMETRY_AUTOMATION_WORK_ORDERS.md` §3.2). Without this, a gateway
reconnecting after network loss corrupts every aggregate built on the hypertable.

### T-03 — A suspicious reading is quarantined, not served

- **Given** a measurement arrives with `quality = 'suspect'` or `'invalid'`,
- **When** it is ingested,
- **Then** it is stored with that quality and a `quarantine_reason`,
- **And** it MUST NOT appear in `/latest`, feed a policy decision, or drive automation,
- **And** it MUST NOT be silently discarded — the row remains as evidence
  (`AGENTS.md` §8).

*Blocked by:* the simulator hardcodes `quality: "ok"` and cannot emit `suspect` or
`invalid`. Drive this with a hand-crafted `mosquitto_pub` until the simulator is fixed.

### T-04 — A malformed payload is rejected without killing the consumer

- **Given** the ingest consumer is running,
- **When** a message arrives that is not valid JSON, or violates `iot-measurement.v1`
  (unknown `sensorType`, `quality` outside the enum, missing `messageId`),
- **Then** it is rejected and recorded,
- **And** the consumer stays alive and continues processing later messages.

*Rationale:* one bad device must not stop telemetry for the whole farm.

### T-05 — Unit must match sensor type

- **Given** a sensor of type `air_temperature` whose unit is `celsius`,
- **When** a measurement arrives claiming `unit = 'percent'`,
- **Then** it is rejected or quarantined, never stored as valid
  (`docs/07_DATA_MODEL_GUIDE.md`, "Measurement unit must match sensor type").

### T-06 — Authorization on read

- **Given** player A leases `plot-001` and player B leases nothing,
- **When** player B calls `GET /api/v1/telemetry/plots/plot-001/latest`,
- **Then** the request is refused,
- **And** the refusal does not reveal whether `plot-001` exists
  (`docs/07_DATA_MODEL_GUIDE.md`, opaque public identifiers; `AGENTS.md` §6).

## 4. Automation commands

### A-01 — A safe player request produces exactly one command

- **Given** player A holds an active lease on `plot-001` with a healthy pump,
- **And** soil moisture is below the policy threshold,
- **When** player A submits `request_extra_watering` (`docs/15_ACTION_CATALOG.md`),
- **Then** the policy returns `accepted_for_automation` with a human-readable reason,
- **And** exactly one `automation_commands` row is created with
  `source = 'player_request'`, a `source_request_id`, the deciding `policy_id` +
  `policy_version`, and an `idempotency_key`,
- **And** the command is published to `realfarm/plots/plot-001/commands`.

### A-02 — Duplicate submissions do not double-run the pump

- **Given** a request carrying `idempotencyKey` `k-1` has produced a command,
- **When** the same `idempotencyKey` is submitted again (impatient double-tap, client
  retry),
- **Then** no second command is created,
- **And** the caller receives the original decision.

*Rationale:* `automation_commands.idempotency_key` is unique. This is the difference
between watering a plot once and flooding it.

### A-03 — Requested duration is capped server-side

- **Given** `actuators.max_duration_seconds` for the pump is 120,
- **When** a request asks for 3600 seconds,
- **Then** the command is created with a duration ≤ 120, or rejected with a reason,
- **And** the cap is never taken from client input (`docs/15_ACTION_CATALOG.md` §4.1).

### A-04 — An acknowledged command reaches a final state

- **Given** a command was published,
- **When** the gateway/simulator publishes an ack on `realfarm/plots/{plot_id}/ack`,
- **Then** the command moves `published → acknowledged → running → succeeded`,
- **And** `actual_duration_seconds` and `completed_at` are recorded.

### A-05 — An unacknowledged command times out

- **Given** a command was published,
- **When** no ack arrives within the timeout,
- **Then** the command becomes `timed_out`, not `succeeded`, and the failure is recorded
  as `COMMAND_ACK_TIMEOUT` (`docs/08_CODING_STANDARDS.md`),
- **And** it is not reported to the player as completed (`AGENTS.md` §7 — the UI must
  never assume a request executed until the backend reports it).

*Blocked by:* the simulator always acks `succeeded` after ~2s and cannot simulate silence.

### A-06 — The watchdog stops a runaway actuator

- **Given** a running command whose `watchdog_deadline_at` has passed,
- **When** the watchdog job runs,
- **Then** a stop is issued and the command becomes `stopped_by_watchdog`,
- **And** this happens even if the process that created the command has died — the
  deadline is stored, not held in memory
  (`docs/17_ERD_TELEMETRY_AUTOMATION_WORK_ORDERS.md` §5).

*Blocked by:* the simulator cannot simulate a non-terminating actuator.

### A-07 — Emergency automation overrides player preference

- **Given** player A submitted `skip_scheduled_watering`,
- **And** soil moisture then falls to a crop-loss threshold,
- **When** emergency automation evaluates the plot,
- **Then** a watering command is issued with `source = 'emergency'` and a reason,
- **And** the player is shown why their preference was overridden
  (`AGENTS.md` §2 — safety overrides preference).

### A-08 — A player cannot drive a restricted actuator directly

- **Given** player A holds an active lease,
- **When** player A submits `request_treatment` with a dosage parameter,
- **Then** the result is `requires_expert_review`, never `accepted_for_automation`,
- **And** no `automation_commands` row is created,
- **And** the dosage parameter is not honored from player input
  (`docs/15_ACTION_CATALOG.md` §4.3; `AGENTS.md` §2).

### A-09 — Every command records who caused it

- **Given** any command in `automation_commands`,
- **Then** `source` is exactly one of `automation`, `operator`, `player_request`,
  `emergency`,
- **And** `reason` is present and human-readable,
- **And** a `player_request` command has a `source_request_id`
  (`AGENTS.md` §8; ADR-0003).

## 5. Coverage against the module rules

| Rule (`AGENTS.md` §8) | Scenario |
|---|---|
| Player requests pass through the policy engine | A-01, A-08 |
| Gateway acknowledges and reports final device state | A-04, A-05 |
| Commands require idempotency keys | A-02 |
| Watchdog limits on actuators | A-03, A-06 |
| Record command source | A-09 |
| Sensor values include timestamp, identity, unit, quality | T-01 |
| Invalid/suspicious values quarantined, never silently valid | T-03, T-04, T-05 |
| Simulator implements the same contract as the gateway | blocked — see §6 |

## 6. Open questions (for cross-review with Học / Bảo)

1. What is the ack timeout before `timed_out` (A-05)?
2. What soil-moisture threshold counts as an emergency (A-07)? Agronomy input needed.
3. Should quarantined rows raise an `Incident` after N consecutive suspect readings from
   one sensor, or stay silent until an operator looks?
4. Does the watchdog run as a durable job (`durable_jobs` in
   `docs/07_DATA_MODEL_GUIDE.md`) or as a broker-side rule? Infra ownership (Bảo).
5. `09_VALIDATION_STRATEGY.md` rules out a committed test tree — do these scenarios stay
   manual, or do the Weeks 7-8 IoT flows justify an ADR to add a simulator-driven
   scenario runner? The failure paths (A-05, A-06) are painful to check by hand.
