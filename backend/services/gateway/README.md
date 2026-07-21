# Gateway

The gateway connects MQTT, sensors, actuators, and camera/media capture. It is the only
component allowed to drive real hardware.

> **Status: subscribe-only skeleton.** It connects to the broker and logs every command on
> `realfarm/plots/+/commands`, and there is now a `gateway` service in
> `docker-compose.yml`. It does not drive hardware, honor idempotency keys, enforce
> watchdog limits, or acknowledge commands yet — those land in Weeks 7-8
> (`docs/10_ROADMAP_16_WEEKS.md`). Until then `backend/services/simulator` is the reference
> implementation of the contract below — a first-class component, not a temporary mock
> (`AGENTS.md` §2). Both import their topics and connection from the shared `common/mqtt.py`.

## Responsibilities

- read device data;
- normalize units;
- attach timestamp and device identity;
- publish telemetry;
- receive validated commands;
- enforce local safety limits;
- acknowledge commands;
- report final device state;
- buffer temporarily during network loss.

## Contract

The gateway and the simulator MUST implement the **same** contract (`AGENTS.md` §8), so
that swapping one for the other changes nothing upstream. That contract has two halves.

### Payload

Telemetry follows `packages/contracts/schemas/iot-measurement.v1.json`: one measurement
per message, carrying `messageId`, `deviceId`, `sensorType`, `value`, `unit`,
`measuredAt`, and `quality`.

`quality` MUST be one of `valid`, `suspect`, or `invalid`. The gateway MUST NOT drop a
suspicious reading or relabel it as valid — the backend quarantines it
(`docs/17_ERD_TELEMETRY_AUTOMATION_WORK_ORDERS.md` §3.3). Filtering at the edge would
destroy the evidence an incident review needs.

### Topics

| Topic | Direction | Purpose |
|---|---|---|
| `realfarm/plots/{plot_id}/telemetry` | gateway → backend | sensor readings |
| `realfarm/plots/{plot_id}/commands` | backend → gateway | validated actuator commands |
| `realfarm/plots/{plot_id}/ack` | gateway → backend | acknowledgement and final state |

See `backend/services/simulator/README.md` for the message shapes currently on the wire.

## Rules this component must not break

From `AGENTS.md` §8 and `docs/02_BUSINESS_RULES.md`:

- **Commands arrive validated.** The gateway never evaluates player intent; the policy
  engine already did (ADR-0003). Its job is to execute or refuse, not to judge.
- **Acknowledge every command** and report the final device state. A command with no ack
  becomes `timed_out` upstream — silence is a failure, not a success.
- **Honor idempotency keys.** A redelivered command with a key already seen MUST NOT run
  the actuator a second time.
- **Enforce watchdog limits locally.** The ceiling is stored upstream in
  `actuators.max_duration_seconds`, but the gateway MUST stop an actuator on its own if
  the backend disappears mid-run. A pump that outlives its network connection is the
  failure this guards against.
- **Every sensor value carries** timestamp, device identity, unit, and quality status.
- **Buffer during network loss** and replay on reconnect; `messageId` makes replay safe.

## Run

The skeleton subscribes and logs; it does not drive hardware yet.

```bash
docker compose up -d mqtt gateway
docker compose logs -f gateway
```

Watch live traffic (the simulator drives the same topics today):

```bash
docker compose exec mqtt mosquitto_sub -t 'realfarm/#' -v
```

When implementing hardware behavior, keep the gateway and
`backend/services/simulator/src/main.py` in step — both import from `common/mqtt.py`, so
the contract stays in one place. If the two drift, the simulator stops being a valid
stand-in and every test built on it becomes misleading.
