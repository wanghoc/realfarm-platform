# IoT Simulator

The simulator is mandatory, not a temporary mock.

It must:

- publish the same telemetry schema as the gateway;
- subscribe to the same command topics;
- send acknowledgements;
- simulate device state and failure;
- support deterministic scenarios for smoke checks and demo validation;
- simulate offline and suspicious-sensor conditions.

Connection settings and topic construction come from the shared `common/mqtt.py`
(`backend/services/common`), which the gateway imports too — the same contract in
one place (`AGENTS.md` §8).

## Run

```bash
docker compose up -d mqtt simulator      # with the stack (starts the broker too)
docker compose logs -f simulator
```

Standalone against a local broker — run from `backend/services` so the shared
`common/` package is importable:

```bash
cd backend/services
pip install -r simulator/requirements.txt
MQTT_HOST=localhost python -m simulator.src.main
```
