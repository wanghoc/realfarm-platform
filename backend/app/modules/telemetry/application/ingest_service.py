"""Telemetry ingest and latest-reading reads.

A redelivered message (same ``messageId`` at the same ``measuredAt``) must not create a
second row. Idempotency rests on the composite primary key, not a read-then-write, so two
concurrent inserts of the same message cannot both succeed (``AGENTS.md`` §8) — the
duplicate raises ``IntegrityError`` and is absorbed here.
"""

import structlog
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.telemetry.api.schemas import IotMeasurementV1, Quality
from app.modules.telemetry.domain.measurement_model import Measurement

log = structlog.get_logger()


async def persist_measurement(
    session: AsyncSession, measurement: IotMeasurementV1
) -> tuple[str, bool]:
    """Persist one measurement idempotently.

    Returns ``(status, is_new)``. ``status`` is ``"accepted"`` for a valid reading and
    ``"quarantined"`` for a suspect/invalid one (``AGENTS.md`` §8). ``is_new`` is ``False``
    when the message was already ingested.
    """
    is_valid = measurement.quality is Quality.valid
    status = "accepted" if is_valid else "quarantined"
    quarantine_reason = None if is_valid else f"quality={measurement.quality.value}"

    session.add(
        Measurement(
            measured_at=measurement.measured_at,
            message_id=measurement.message_id,
            device_id=measurement.device_id,
            plot_id=measurement.plot_id,
            sensor_type=measurement.sensor_type.value,
            value=measurement.value,
            unit=measurement.unit,
            quality=measurement.quality.value,
            quarantine_reason=quarantine_reason,
            signature=measurement.signature,
        )
    )
    try:
        await session.flush()
    except IntegrityError:
        await session.rollback()
        log.info(
            "telemetry.duplicate_ignored",
            message_id=measurement.message_id,
            plot_id=measurement.plot_id,
        )
        return status, False

    log.info(
        "telemetry.ingested",
        ingest_status=status,
        message_id=measurement.message_id,
        plot_id=measurement.plot_id,
        sensor_type=measurement.sensor_type.value,
        quality=measurement.quality.value,
    )
    return status, True


async def latest_valid_by_plot(
    session: AsyncSession, plot_id: str, lookback: int = 200
) -> list[Measurement]:
    """Return the latest valid reading per sensor type for a plot.

    Only ``quality='valid'`` rows feed reads that drive UI or automation — a quarantined
    row is evidence, not a measurement (``AGENTS.md`` §8).
    """
    result = await session.execute(
        select(Measurement)
        .where(Measurement.plot_id == plot_id, Measurement.quality == "valid")
        .order_by(Measurement.measured_at.desc())
        .limit(lookback)
    )
    newest_by_sensor: dict[str, Measurement] = {}
    for row in result.scalars():
        newest_by_sensor.setdefault(row.sensor_type, row)
    return list(newest_by_sensor.values())
