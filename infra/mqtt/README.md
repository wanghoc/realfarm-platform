# MQTT

The RealFarm broker (Eclipse Mosquitto 2.x, `docker-compose.yml` service `mqtt`)
carries telemetry from the field and commands to it. The simulator and the real gateway
MUST speak the **same** topic and QoS contract (`AGENTS.md` §8), so that swapping one for
the other changes nothing upstream. This document is that contract.

## Topic convention

Topics are **plot-scoped**, because the plot is the unit a lease, a player, and the
policy engine all address. A single gateway may serve several plots, but that is a
deployment detail; the wire is organised by plot, not by gateway.

```text
realfarm/plots/{plot_id}/telemetry     edge    -> backend   sensor readings
realfarm/plots/{plot_id}/commands      backend -> edge      actuator commands
realfarm/plots/{plot_id}/ack           edge    -> backend   acknowledgements / final state
```

| Topic | Direction | Purpose | Payload |
|---|---|---|---|
| `realfarm/plots/{plot_id}/telemetry` | edge → backend | sensor readings | `iot-measurement.v1` |
| `realfarm/plots/{plot_id}/commands` | backend → edge | validated actuator commands | versioned command contract |
| `realfarm/plots/{plot_id}/ack` | edge → backend | acknowledgement and final device state | ack payload |

`{plot_id}` is the plot's identifier (e.g. `plot-001`). A gateway serving many plots
subscribes to commands with the wildcard `realfarm/plots/+/commands`.

> This replaces the earlier `realfarm/v1/gateways/{gatewayId}/…` proposal, which never
> matched the code. The simulator (`backend/services/simulator`) has always published on
> the plot-scoped topics above; the convention now follows the implementation.

## Sensors (MVP)

The simulator publishes three basic sensors per plot, which are the MVP set:

| `sensorType` | Unit | Notes |
|---|---|---|
| `air_temperature` | celsius | greenhouse air temperature |
| `air_humidity` | percent | relative humidity |
| `soil_moisture` | percent | root-zone moisture |

`light` and `ph` exist in the `iot-measurement.v1` enum but are optional hardware and
are out of the MVP sensor set.

## Quality of Service

**Every RealFarm topic uses QoS 1 (at-least-once).** A dropped telemetry reading or a
dropped command is a real loss — silence upstream is treated as failure, not success —
so at-most-once (QoS 0) is not acceptable. QoS 2 is avoided: its four-step handshake adds
latency and broker state the platform does not need, because duplicates are already made
safe idempotently (telemetry deduplicates on `messageId`; commands carry an idempotency
key, `AGENTS.md` §8).

Because QoS 1 can redeliver, **consumers MUST be idempotent** — the contract makes this
possible, but the consumer enforces it.

## Broker configuration

`mosquitto.conf` is tuned for the QoS-1 contract above:

- `persistence true` — in-flight and queued QoS-1 messages survive a broker restart,
  so a message accepted from a publisher is not lost when the broker bounces.
- `max_inflight_messages` / `max_queued_messages` — bound the per-client QoS-1 window and
  the queue held for a temporarily offline subscriber.
- `allow_anonymous true` — development only. Outside local development the broker MUST use
  authenticated clients (per-service credentials or mTLS); this is a follow-up, not part
  of the MVP transport bring-up.

For production the persistence directory (`/mosquitto/data`) SHOULD be mounted on a
durable volume so it also survives container recreation, not only a restart.

## Contract review: simulator ↔ gateway

Both edge implementations MUST match on all three axes below. The simulator is the
reference today; the gateway (`backend/services/gateway`) MUST implement the identical
contract before it can stand in for the simulator (`AGENTS.md` §8).

| Axis | Value | Simulator | Gateway |
|---|---|---|---|
| Topics | `realfarm/plots/{plot_id}/{telemetry,commands,ack}` | ✅ publishes/subscribes | must match |
| QoS | 1 on every topic | ✅ | must match |
| Telemetry payload | `iot-measurement.v1` | payload alignment lands with telemetry persistence (Weeks 7-8, `docs/10_ROADMAP_16_WEEKS.md`) | must match |

## Watch live traffic

```bash
docker compose up -d mqtt simulator
docker compose exec mqtt mosquitto_sub -t 'realfarm/#' -v
```
