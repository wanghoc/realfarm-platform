"""
CropCycle ORM model and State Machine.
"""

import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum as SqlEnum, Index, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class CropCycleStatus(str, enum.Enum):
    """States of a CropCycle."""

    PLANNED = "planned"
    PLANTED = "planted"
    GROWING = "growing"
    AWAITING_HARVEST = "awaiting_harvest"
    HARVESTED = "harvested"
    CLOSED = "closed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CropCycle(Base):
    """
    Represents one crop lifecycle on one plot.
    """

    __tablename__ = "crop_cycles"

    __table_args__ = (
        Index(
            "ix_crop_cycles_active_plot",
            "plot_id",
            unique=True,
            sqlite_where=text("status NOT IN ('closed', 'failed', 'cancelled')"),
            postgresql_where=text("status NOT IN ('closed', 'failed', 'cancelled')")
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plot_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    lease_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    crop_catalog_id: Mapped[str] = mapped_column(String(36), nullable=False)

    status: Mapped[CropCycleStatus] = mapped_column(
        SqlEnum(CropCycleStatus), nullable=False, default=CropCycleStatus.PLANNED
    )

    planted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expected_harvest_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    harvested_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=lambda: datetime.now(UTC),
    )

    # --- State Machine Transitions ---

    def plant(self, existing_cycles: list["CropCycle"]) -> None:
        """
        Move from PLANNED to PLANTED.
        Must be validated against business rule:
        'A plot MUST NOT have more than one active crop cycle at the same time.'
        """
        if self.status != CropCycleStatus.PLANNED:
            raise ValueError(f"Cannot plant from status {self.status}")

        terminal_states = {
            CropCycleStatus.CLOSED,
            CropCycleStatus.FAILED,
            CropCycleStatus.CANCELLED,
        }
        for cycle in existing_cycles:
            if cycle.id != self.id and cycle.status not in terminal_states:
                raise ValueError(f"Plot {self.plot_id} already has an active crop cycle.")

        self.status = CropCycleStatus.PLANTED
        self.planted_at = datetime.now(UTC)

    def start_growing(self) -> None:
        """Move from PLANTED to GROWING."""
        if self.status != CropCycleStatus.PLANTED:
            raise ValueError(f"Cannot start growing from status {self.status}")
        self.status = CropCycleStatus.GROWING

    def ready_for_harvest(self) -> None:
        """Move from GROWING to AWAITING_HARVEST."""
        if self.status != CropCycleStatus.GROWING:
            raise ValueError(f"Cannot await harvest from status {self.status}")
        self.status = CropCycleStatus.AWAITING_HARVEST

    def harvest(self) -> None:
        """Move from AWAITING_HARVEST to HARVESTED."""
        if self.status != CropCycleStatus.AWAITING_HARVEST:
            raise ValueError(f"Cannot harvest from status {self.status}")
        self.status = CropCycleStatus.HARVESTED
        self.harvested_at = datetime.now(UTC)

    def close(self) -> None:
        """Move from HARVESTED to CLOSED (finalizing cycle)."""
        if self.status != CropCycleStatus.HARVESTED:
            raise ValueError(f"Cannot close from status {self.status}")
        self.status = CropCycleStatus.CLOSED

    def fail(self) -> None:
        """Mark the crop cycle as failed (e.g. natural disaster, disease)."""
        if self.status in [CropCycleStatus.CLOSED, CropCycleStatus.CANCELLED]:
            raise ValueError(f"Cannot fail from terminal status {self.status}")
        self.status = CropCycleStatus.FAILED

    def cancel(self) -> None:
        """Cancel the crop cycle manually."""
        if self.status in [CropCycleStatus.CLOSED, CropCycleStatus.FAILED]:
            raise ValueError(f"Cannot cancel from terminal status {self.status}")
        self.status = CropCycleStatus.CANCELLED
