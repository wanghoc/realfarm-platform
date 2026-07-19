"""Telemetry module router.

Receives and serves sensor measurements from IoT devices.
Invalid or suspicious values are quarantined — never silently treated as valid.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.security import TokenPayload, get_current_user
from app.modules.telemetry.api.schemas import IngestAck, IotMeasurementV1, Quality

router = APIRouter(prefix="/telemetry", tags=["telemetry"])


@router.post(
    "/ingest",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=IngestAck,
    response_model_by_alias=True,
    summary="Ingest a single IoT measurement (stub)",
)
async def ingest_measurement(measurement: IotMeasurementV1) -> IngestAck:
    """
    Accept one measurement in the ``realfarm.iot-measurement.v1`` format.

    Week-3 stub: it validates the contract at the boundary and classifies the
    reading, but does NOT persist. Persistence to the TimescaleDB hypertable,
    ``messageId`` idempotency, and unit/sensor-type checks land in Weeks 7-8
    (``docs/10_ROADMAP_16_WEEKS.md``).

    A suspect or invalid reading is quarantined, never silently accepted as a
    valid measurement (``AGENTS.md`` §8).

    TODO(security): authenticate the sending device (device token or mTLS)
    before this ingests anything real — a gateway is not a logged-in user, so
    the user-JWT dependency used elsewhere in this module does not fit here.
    """
    if measurement.quality is Quality.valid:
        return IngestAck(message_id=measurement.message_id, status="accepted")
    return IngestAck(
        message_id=measurement.message_id,
        status="quarantined",
        reason=f"quality={measurement.quality.value}",
    )


@router.get("/plots/{plot_id}/latest")
async def get_latest_telemetry(
    plot_id: str,
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
) -> dict:
    """
    Return latest sensor readings for a plot.
    Each measurement includes: timestamp, device id, unit, quality status.
    TODO: query TimescaleDB hypertable.
    """
    return {"plot_id": plot_id, "measurements": []}
