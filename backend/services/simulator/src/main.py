"""
RealFarm IoT simulator.

Publishes synthetic sensor telemetry over MQTT at regular intervals and listens
for commands using the same topic contract as the real gateway. Connection and
topic construction come from ``common.mqtt`` so the simulator and the gateway
cannot drift apart (``AGENTS.md`` §8).

MQTT topic schema:
  realfarm/plots/{plot_id}/telemetry     sensor readings
  realfarm/plots/{plot_id}/commands      commands received from API
  realfarm/plots/{plot_id}/ack           acknowledgements published by simulator
"""

import asyncio
import json
import os
import random
from datetime import UTC, datetime

import aiomqtt
from common.mqtt import (
    QOS,
    MqttConfig,
    ack_topic,
    client,
    commands_topic,
    plot_id_from_topic,
    telemetry_topic,
)

TELEMETRY_INTERVAL_SECONDS = int(os.getenv("TELEMETRY_INTERVAL_SECONDS", "10"))

SIMULATED_PLOTS = ["plot-001", "plot-002"]


def generate_telemetry(plot_id: str) -> dict:
    """Generate plausible sensor readings for a greenhouse plot."""
    return {
        "device_id": f"sim-gateway-{plot_id}",
        "plot_id": plot_id,
        "timestamp": datetime.now(UTC).isoformat(),
        "source": "simulator",
        "measurements": [
            {
                "metric": "air_temperature",
                "value": round(random.uniform(22.0, 30.0), 1),
                "unit": "celsius",
                "quality": "ok",
            },
            {
                "metric": "air_humidity",
                "value": round(random.uniform(55.0, 80.0), 1),
                "unit": "percent",
                "quality": "ok",
            },
            {
                "metric": "soil_moisture",
                "value": round(random.uniform(30.0, 70.0), 1),
                "unit": "percent",
                "quality": "ok",
            },
        ],
    }


async def publish_telemetry(mqtt: aiomqtt.Client) -> None:
    """Publish telemetry for all simulated plots at regular intervals."""
    while True:
        for plot_id in SIMULATED_PLOTS:
            payload = generate_telemetry(plot_id)
            topic = telemetry_topic(plot_id)
            await mqtt.publish(topic, json.dumps(payload), qos=QOS)
            print(f"[simulator] Published telemetry to {topic}")
        await asyncio.sleep(TELEMETRY_INTERVAL_SECONDS)


async def listen_commands(mqtt: aiomqtt.Client) -> None:
    """Listen for actuator commands and publish final acknowledgements."""
    for plot_id in SIMULATED_PLOTS:
        await mqtt.subscribe(commands_topic(plot_id), qos=QOS)
        print(f"[simulator] Subscribed to commands for {plot_id}")

    async for message in mqtt.messages:
        topic = str(message.topic)
        try:
            command = json.loads(message.payload)
        except (json.JSONDecodeError, UnicodeDecodeError):
            # payload is bytes; non-UTF-8 raises UnicodeDecodeError, which is
            # NOT a JSONDecodeError. Swallow both so junk cannot kill the task.
            print(f"[simulator] Malformed command on {topic}")
            continue

        if not isinstance(command, dict):
            # Valid JSON that is not an object (e.g. 123, "x", []) has no
            # .get(); guard before command.get(...) below would raise.
            print(f"[simulator] Ignoring non-object command on {topic}")
            continue

        print(f"[simulator] Received command: {command}")

        await asyncio.sleep(2)
        plot_id = plot_id_from_topic(topic)
        ack = {
            "command_id": command.get("command_id", "unknown"),
            "plot_id": plot_id,
            "status": "succeeded",
            "timestamp": datetime.now(UTC).isoformat(),
        }
        await mqtt.publish(ack_topic(plot_id), json.dumps(ack), qos=QOS)
        print(f"[simulator] Sent ACK for command {ack['command_id']}")


async def main() -> None:
    config = MqttConfig.from_env()
    print(f"[simulator] Connecting to MQTT broker at {config.host}:{config.port}")
    async with client(config) as mqtt:
        print("[simulator] Connected. Starting telemetry and command listener.")
        await asyncio.gather(
            publish_telemetry(mqtt),
            listen_commands(mqtt),
        )


if __name__ == "__main__":
    asyncio.run(main())
