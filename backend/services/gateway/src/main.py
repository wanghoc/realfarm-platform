"""
RealFarm IoT gateway (skeleton).

Bridges MQTT, sensors, actuators, and camera to real hardware. Only this
component is allowed to drive real hardware.

Status: skeleton. It connects to the broker and subscribes to the command
topic, logging every command it receives. It does NOT drive hardware, enforce
watchdog limits, honor idempotency keys, or acknowledge commands yet — those
land with telemetry and the watchdog in Weeks 7-8
(``docs/10_ROADMAP_16_WEEKS.md``). Until then ``backend/services/simulator`` is
the reference implementation of the same contract (``AGENTS.md`` §8), which is
why both import their topics and connection from ``common.mqtt``.
"""

import asyncio
import json

import aiomqtt
from common.mqtt import QOS, MqttConfig, client, commands_topic, plot_id_from_topic

# A single gateway serves every plot it is wired to, so it subscribes with a
# wildcard rather than a fixed list of plots.
COMMANDS_WILDCARD = commands_topic("+")


async def listen_commands(mqtt: aiomqtt.Client) -> None:
    """Subscribe to the command topic and log every command received."""
    await mqtt.subscribe(COMMANDS_WILDCARD, qos=QOS)
    print(f"[gateway] Subscribed to {COMMANDS_WILDCARD}")

    async for message in mqtt.messages:
        topic = str(message.topic)
        try:
            command = json.loads(message.payload)
        except (json.JSONDecodeError, UnicodeDecodeError):
            # payload is bytes; non-UTF-8 raises UnicodeDecodeError, which is
            # NOT a JSONDecodeError. Anonymous publishers can send garbage, so
            # both must be swallowed rather than kill the listener task.
            print(f"[gateway] Malformed command on {topic}")
            continue

        plot_id = plot_id_from_topic(topic)
        # TODO(weeks 7-8): reject a redelivered idempotency key, drive the
        # actuator under its watchdog ceiling, then publish an ack on
        # realfarm/plots/{plot_id}/ack with the final device state. A command
        # with no ack becomes timed_out upstream — silence is a failure.
        print(f"[gateway] Received command for {plot_id}: {command}")


async def main() -> None:
    config = MqttConfig.from_env()
    print(f"[gateway] Connecting to MQTT broker at {config.host}:{config.port}")
    async with client(config) as mqtt:
        print("[gateway] Connected. Listening for commands.")
        await listen_commands(mqtt)


if __name__ == "__main__":
    asyncio.run(main())
