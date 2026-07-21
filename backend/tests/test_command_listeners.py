"""Regression tests: junk MQTT payloads must not crash the command listeners.

Drives the real ``listen_commands`` coroutines from the gateway and simulator
with the exact byte payloads from the PR #69 review — non-UTF-8 bytes (which
raise ``UnicodeDecodeError``, not ``JSONDecodeError``) and valid-JSON-that-is-
not-an-object — and asserts the loop survives every one instead of the task
dying. A dev broker allows anonymous publishers, so this is untrusted input.
"""

import asyncio

from gateway.src.main import listen_commands as gateway_listen
from simulator.src.main import listen_commands as simulator_listen

COMMANDS_TOPIC = "realfarm/plots/plot-001/commands"

# Non-UTF-8 bytes + malformed JSON + valid JSON that is not an object.
JUNK_PAYLOADS = [
    b"\x80\x81\x82",  # invalid UTF-8 -> UnicodeDecodeError
    b'"\xff"',  # invalid UTF-8 -> UnicodeDecodeError
    b"not-json",  # JSONDecodeError
    b"123",  # valid JSON, not an object
    b'"x"',  # valid JSON, not an object
    b"[]",  # valid JSON, not an object
]


class _FakeMessage:
    def __init__(self, topic: str, payload: bytes):
        self.topic = topic
        self.payload = payload


class _FakeMessages:
    """Minimal stand-in for ``aiomqtt.Client.messages`` (an async iterator)."""

    def __init__(self, messages):
        self._messages = list(messages)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if not self._messages:
            raise StopAsyncIteration
        return self._messages.pop(0)


class _FakeClient:
    """Records publishes; never touches a real broker."""

    def __init__(self, payloads):
        self.messages = _FakeMessages(_FakeMessage(COMMANDS_TOPIC, p) for p in payloads)
        self.published: list[tuple] = []

    async def subscribe(self, topic, qos=None):
        return None

    async def publish(self, topic, payload, qos=None):
        self.published.append((topic, payload))


def test_gateway_survives_junk_commands():
    client = _FakeClient(JUNK_PAYLOADS)
    asyncio.run(gateway_listen(client))  # must return, not raise


def test_simulator_survives_junk_commands():
    client = _FakeClient(JUNK_PAYLOADS)
    asyncio.run(simulator_listen(client))  # must return, not raise
    # Junk is dropped before the ack path, so nothing is published.
    assert client.published == []
