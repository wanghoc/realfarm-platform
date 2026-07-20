# IoT Simulator

The simulator is mandatory, not a temporary mock. Hardware unavailability must not block
development (`AGENTS.md` §2), so the simulator — not the gateway — is what the backend is
built and tested against today. `backend/services/gateway` is still an empty placeholder.

It must:

- publish the same telemetry schema as the gateway;
- subscribe to the same command topics;
- send acknowledgements;
- simulate device state and failure;
- support deterministic scenarios for smoke checks and demo validation;
- simulate offline and suspicious-sensor conditions.

## Run

With the stack (recommended — starts the MQTT broker too):

```bash
docker compose up -d mqtt simulator
docker compose logs -f simulator
```

Standalone against a local broker:

```bash
cd backend/services/simulator
pip install -r requirements.txt
MQTT_HOST=localhost python -m src.main
```

Watch what it publishes:

```bash
docker compose exec mqtt mosquitto_sub -t 'realfarm/#' -v
```

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `MQTT_HOST` | `localhost` | Broker hostname. `docker-compose.yml` sets this to `mqtt`. |
| `MQTT_PORT` | `1883` | Broker port. |
| `TELEMETRY_INTERVAL_SECONDS` | `10` | Seconds between telemetry rounds. |

Simulated plots are hardcoded in `src/main.py` (`SIMULATED_PLOTS = ["plot-001", "plot-002"]`).

## Topics

| Topic | Direction | Purpose |
|---|---|---|
| `realfarm/plots/{plot_id}/telemetry` | simulator → backend | sensor readings |
| `realfarm/plots/{plot_id}/commands` | backend → simulator | actuator commands |
| `realfarm/plots/{plot_id}/ack` | simulator → backend | acknowledgement and final state |

All traffic uses QoS 1.

## Current message shapes

**Telemetry** (`src/main.py:generate_telemetry`) — one message per plot, batching several
readings:

```json
{
  "device_id": "sim-gateway-plot-001",
  "plot_id": "plot-001",
  "timestamp": "2026-07-15T09:30:00+00:00",
  "source": "simulator",
  "measurements": [
    { "metric": "air_temperature", "value": 26.4, "unit": "celsius", "quality": "ok" }
  ]
}
```

**Ack** (published ~2s after a command, always success):

```json
{
  "command_id": "cmd-123",
  "plot_id": "plot-001",
  "status": "succeeded",
  "timestamp": "2026-07-15T09:30:02+00:00"
}
```

## Known drift from `iot-measurement.v1` — do not build on this yet

The telemetry above does **not** satisfy
`packages/contracts/schemas/iot-measurement.v1.json`, which is the contract the backend
ingest and the real gateway are required to speak (`AGENTS.md` §8). Concretely:

| Contract requires | Simulator currently sends |
|---|---|
| one measurement per message | a batched `measurements[]` array |
| `messageId` (required) | absent — nothing to dedupe replays on |
| `deviceId`, `sensorType`, `measuredAt` (camelCase) | `device_id`, `metric`, `timestamp` (snake_case) |
| `quality` ∈ `valid` \| `suspect` \| `invalid` | `"ok"` — **not a valid enum value** |
| `plotId` optional, `signature` optional | `plot_id`, plus an extra `source` field |
| `additionalProperties: false` | `source` would be rejected |

Until this is reconciled, the simulator is a **transport** demo (topics, QoS, ack timing
are right) but not a **payload** demo. Telemetry ingest cannot be written against these
messages without silently accepting a shape the real gateway will never send.

Two things must also be fixed for the simulator to do the job it exists for:

- **`quality` is hardcoded `"ok"`.** The simulator is required to simulate
  suspicious-sensor conditions, but it currently cannot emit `suspect` or `invalid`, so
  the backend's quarantine path (`docs/17_ERD_TELEMETRY_AUTOMATION_WORK_ORDERS.md` §3.3)
  has nothing to exercise it.
- **Every ack is `succeeded` after a fixed 2s sleep.** There is no way to simulate
  `rejected_by_gateway`, `timed_out`, `failed`, or `stopped_by_watchdog`, so the command
  failure paths in `docs/18_ACCEPTANCE_TESTS_TELEMETRY_AUTOMATION.md` cannot run yet.

Aligning the payload and adding failure scenarios lands with telemetry persistence and
the watchdog in **Weeks 7-8** (`docs/10_ROADMAP_16_WEEKS.md`). It is tracked as an open
question in `docs/17_ERD_TELEMETRY_AUTOMATION_WORK_ORDERS.md` §6, and the scenarios it
must satisfy are specified in `docs/18_ACCEPTANCE_TESTS_TELEMETRY_AUTOMATION.md`.
