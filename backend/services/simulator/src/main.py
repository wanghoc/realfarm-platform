"""
RealFarm IoT simulator.

Publishes synthetic sensor telemetry over MQTT at regular intervals and listens
for commands using the same topic contract as the real gateway.

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

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
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


async def publish_telemetry(client: aiomqtt.Client) -> None:
    """Publish telemetry for all simulated plots at regular intervals."""
    while True:
        for plot_id in SIMULATED_PLOTS:
            payload = generate_telemetry(plot_id)
            topic = f"realfarm/plots/{plot_id}/telemetry"
            await client.publish(topic, json.dumps(payload), qos=1)
            print(f"[simulator] Published telemetry to {topic}")
        await asyncio.sleep(TELEMETRY_INTERVAL_SECONDS)


async def listen_commands(client: aiomqtt.Client) -> None:
    """Listen for actuator commands and publish final acknowledgements."""
    for plot_id in SIMULATED_PLOTS:
        await client.subscribe(f"realfarm/plots/{plot_id}/commands", qos=1)
        print(f"[simulator] Subscribed to commands for {plot_id}")

    async for message in client.messages:
        topic = str(message.topic)
        try:
            command = json.loads(message.payload)
        except json.JSONDecodeError:
            print(f"[simulator] Malformed command on {topic}")
            continue

        print(f"[simulator] Received command: {command}")

        await asyncio.sleep(2)
        plot_id = topic.split("/")[2]
        ack = {
            "command_id": command.get("command_id", "unknown"),
            "plot_id": plot_id,
            "status": "succeeded",
            "timestamp": datetime.now(UTC).isoformat(),
        }
        await client.publish(f"realfarm/plots/{plot_id}/ack", json.dumps(ack), qos=1)
        print(f"[simulator] Sent ACK for command {ack['command_id']}")


async def main() -> None:
    print(f"[simulator] Connecting to MQTT broker at {MQTT_HOST}:{MQTT_PORT}")
    async with aiomqtt.Client(hostname=MQTT_HOST, port=MQTT_PORT) as client:
        print("[simulator] Connected. Starting telemetry and command listener.")
        await asyncio.gather(
            publish_telemetry(client),
            listen_commands(client),
        )


if __name__ == "__main__":
    asyncio.run(main())
