"""Transport schemas for the telemetry module.

``IotMeasurementV1`` mirrors ``packages/contracts/schemas/iot-measurement.v1.json``
— the contract the gateway and simulator both speak (``AGENTS.md`` §8). The wire
format is camelCase; Python fields stay snake_case and map to the wire via a
camelCase alias generator, so renaming a Python field never changes the contract.
"""

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class SensorType(StrEnum):
    """Allowed sensor types (iot-measurement.v1 `sensorType` enum)."""

    air_temperature = "air_temperature"
    air_humidity = "air_humidity"
    soil_moisture = "soil_moisture"
    light = "light"
    ph = "ph"


class Quality(StrEnum):
    """Reading quality (iot-measurement.v1 `quality` enum)."""

    valid = "valid"
    suspect = "suspect"
    invalid = "invalid"


class _CamelModel(BaseModel):
    """Base model: camelCase wire aliases, reject unknown fields."""

    # extra="forbid" mirrors the contract's `additionalProperties: false`.
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="forbid",
    )


class IotMeasurementV1(_CamelModel):
    """A single IoT measurement — one sensor reading per message, per the contract."""

    message_id: str
    device_id: str
    plot_id: str | None = None
    sensor_type: SensorType
    value: float
    unit: str
    measured_at: datetime
    quality: Quality
    signature: str | None = None


class IngestAck(_CamelModel):
    """Acknowledgement returned by the telemetry ingest endpoint."""

    message_id: str
    status: Literal["accepted", "quarantined"]
    reason: str | None = None
