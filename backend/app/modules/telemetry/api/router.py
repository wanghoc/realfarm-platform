"""Telemetry module router.

Receives and serves sensor measurements from IoT devices.
Invalid or suspicious values are quarantined — never silently treated as valid.
"""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.security import TokenPayload, get_current_user

router = APIRouter(prefix="/telemetry", tags=["telemetry"])


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
