"""
Measurement ORM model — one sensor reading per row.

Stored in the ``measurements`` table, a TimescaleDB hypertable partitioned on
``measured_at`` (see the 0002 migration). Mirrors ``iot-measurement.v1`` plus the
quarantine and ingest-time columns telemetry needs.

Idempotency rests on the composite primary key ``(measured_at, message_id)``: TimescaleDB
requires the partition column in any unique constraint, and a redelivered message carries
the same ``measured_at`` and ``message_id``, so it cannot create a second row
(``AGENTS.md`` §8). Quarantined readings stay in this same table, marked by ``quality`` —
a quarantined row is evidence, not a measurement, and read paths filter ``quality='valid'``.
"""

from datetime import datetime

from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Measurement(Base):
    __tablename__ = "measurements"

    measured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    message_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    device_id: Mapped[str] = mapped_column(String(128), nullable=False)
    plot_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    sensor_type: Mapped[str] = mapped_column(String(32), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(32), nullable=False)
    quality: Mapped[str] = mapped_column(String(16), nullable=False)
    quarantine_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    signature: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    def __repr__(self) -> str:
        return (
            f"<Measurement plot={self.plot_id} sensor={self.sensor_type} "
            f"value={self.value} quality={self.quality} at={self.measured_at}>"
        )
