# Gateway

The gateway connects MQTT, sensors, actuators, and camera/media capture.

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

The gateway contract must match the simulator contract.

## Status

Subscribe-only skeleton. It connects to the broker and logs every command on
`realfarm/plots/+/commands`. It does not drive hardware, honor idempotency keys,
enforce watchdog limits, or acknowledge commands yet (Weeks 7-8,
`docs/10_ROADMAP_16_WEEKS.md`). Until then `backend/services/simulator` is the
reference implementation of the same contract (`AGENTS.md` §8); both import their
topics and connection from the shared `common/mqtt.py`.

## Run

```bash
docker compose up -d mqtt gateway
docker compose logs -f gateway
```
