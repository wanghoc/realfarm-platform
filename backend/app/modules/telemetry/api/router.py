"""Telemetry module router.

Receives and serves sensor measurements from IoT devices.
Invalid or suspicious values are quarantined — never silently treated as valid.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import TokenPayload, get_current_user
from app.modules.telemetry.api.schemas import IngestAck, IotMeasurementV1, Quality
from app.modules.telemetry.application.ingest_service import (
    latest_valid_by_plot,
    persist_measurement,
)

router = APIRouter(prefix="/telemetry", tags=["telemetry"])


@router.post(
    "/ingest",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=IngestAck,
    response_model_by_alias=True,
    summary="Ingest a single IoT measurement",
)
async def ingest_measurement(
    measurement: IotMeasurementV1,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> IngestAck:
    """
    Accept and persist one measurement in the ``realfarm.iot-measurement.v1`` format.

    Validated at the boundary, then written to the ``measurements`` hypertable
    idempotently — a redelivered ``messageId`` does not create a second row. A suspect or
    invalid reading is quarantined, never silently accepted as valid (``AGENTS.md`` §8).

    TODO(security): authenticate the sending device (device token or mTLS) — a gateway is
    not a logged-in user, so the user-JWT dependency used elsewhere does not fit here.
    """
    ingest_status, is_new = await persist_measurement(db, measurement)
    reason = (
        None if measurement.quality is Quality.valid else f"quality={measurement.quality.value}"
    )
    if not is_new:
        reason = "duplicate messageId; already ingested" + (f" ({reason})" if reason else "")
    return IngestAck(message_id=measurement.message_id, status=ingest_status, reason=reason)


@router.get("/plots/{plot_id}/latest")
async def get_latest_telemetry(
    plot_id: str,
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> dict:
    """
    Return the latest valid reading per sensor for a plot.
    Quarantined rows are excluded — a quarantined row is evidence, not a measurement.
    """
    rows = await latest_valid_by_plot(db, plot_id)
    return {
        "plot_id": plot_id,
        "measurements": [
            {
                "sensorType": row.sensor_type,
                "value": row.value,
                "unit": row.unit,
                "measuredAt": row.measured_at.isoformat(),
                "deviceId": row.device_id,
            }
            for row in rows
        ],
    }
