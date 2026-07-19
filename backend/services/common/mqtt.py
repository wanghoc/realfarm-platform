"""Shared MQTT client wrapper for RealFarm IoT edge services.

The simulator and the real gateway MUST speak the same MQTT contract
(``AGENTS.md`` §8), so that swapping one for the other changes nothing upstream.
Centralizing connection config and topic construction here is what makes "same
contract" enforceable in code, instead of by keeping two files in sync by hand.

Topic contract (QoS 1 everywhere):

    realfarm/plots/{plot_id}/telemetry   edge    -> backend   sensor readings
    realfarm/plots/{plot_id}/commands    backend -> edge      actuator commands
    realfarm/plots/{plot_id}/ack         edge    -> backend   acks / final state
"""

import os
from dataclasses import dataclass

import aiomqtt

TOPIC_ROOT = "realfarm/plots"

# Every message on the contract uses QoS 1: at-least-once delivery, deduplicated
# upstream by the contract's ``messageId``. Silence is a failure, not a success.
QOS = 1


def telemetry_topic(plot_id: str) -> str:
    """Topic a plot's sensor readings are published on (edge -> backend)."""
    return f"{TOPIC_ROOT}/{plot_id}/telemetry"


def commands_topic(plot_id: str) -> str:
    """Topic actuator commands are delivered on (backend -> edge).

    Pass ``"+"`` as ``plot_id`` to build the wildcard a gateway subscribes to
    when it serves every plot it is wired to.
    """
    return f"{TOPIC_ROOT}/{plot_id}/commands"


def ack_topic(plot_id: str) -> str:
    """Topic acknowledgements and final device state are published on."""
    return f"{TOPIC_ROOT}/{plot_id}/ack"


def plot_id_from_topic(topic: str) -> str:
    """Extract ``{plot_id}`` from any ``realfarm/plots/{plot_id}/...`` topic."""
    return topic.split("/")[2]


@dataclass(frozen=True)
class MqttConfig:
    """Broker connection settings, read from the environment."""

    host: str = "localhost"
    port: int = 1883

    @classmethod
    def from_env(cls) -> "MqttConfig":
        return cls(
            host=os.getenv("MQTT_HOST", "localhost"),
            port=int(os.getenv("MQTT_PORT", "1883")),
        )


def client(config: MqttConfig | None = None) -> aiomqtt.Client:
    """Return a configured (not yet connected) MQTT client.

    Use it as an async context manager: ``async with client() as mqtt: ...``.

    Auth is intentionally omitted here: the development broker allows anonymous
    access (``infra/mqtt/mosquitto.conf``). Authenticated clients for non-local
    environments are a follow-up (``infra/mqtt/README.md``).
    """
    config = config or MqttConfig.from_env()
    return aiomqtt.Client(hostname=config.host, port=config.port)
