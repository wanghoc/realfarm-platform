"""
Lease ORM model and State Machine.
"""

import enum
import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, String, func, Index, text, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LeaseStatus(str, enum.Enum):
    """States of a Lease."""

    DRAFT = "draft"
    PENDING_PAYMENT_OR_APPROVAL = "pending_payment_or_approval"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    TERMINATED = "terminated"


class ServicePackage(str, enum.Enum):
    """
    Defines the level of service provided for the lease.
    """

    BASIC = "basic"  # Player manages most aspects manually or via paid actions
    FULL_SERVICE = "full_service"  # Operator handles daily tasks based on schedule
    PREMIUM = "premium"  # Full service + guaranteed yields + priority


class HarvestPolicy(str, enum.Enum):
    """
    Defines how the harvest is distributed or handled.
    """

    ALL_TO_PLAYER = "all_to_player"  # Player gets all accepted produce (default)
    SHARED = "shared"  # Yield is shared between farm and player
    MARKET_SELL = "market_sell"  # Farm sells on behalf of player and credits account


class Lease(Base):
    """
    Represents the customer's right to use a plot under a service package.
    """

    __tablename__ = "leases"

    __table_args__ = (
        Index(
            "ix_leases_active_plot", 
            "plot_id", 
            unique=True, 
            sqlite_where=text("status = 'active'"), 
            postgresql_where=text("status = 'active'")
        ),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plot_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    player_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)

    status: Mapped[LeaseStatus] = mapped_column(
        SqlEnum(LeaseStatus), nullable=False, default=LeaseStatus.DRAFT
    )
    service_package: Mapped[ServicePackage] = mapped_column(SqlEnum(ServicePackage), nullable=False)
    harvest_policy: Mapped[HarvestPolicy] = mapped_column(SqlEnum(HarvestPolicy), nullable=False)

    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expected_end_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

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

    def submit_for_approval(self) -> None:
        """Move from DRAFT to PENDING_PAYMENT_OR_APPROVAL."""
        if self.status != LeaseStatus.DRAFT:
            raise ValueError(f"Cannot submit lease from status {self.status}")
        self.status = LeaseStatus.PENDING_PAYMENT_OR_APPROVAL

    def activate(self, existing_leases: list["Lease"]) -> None:
        """
        Move from PENDING_PAYMENT_OR_APPROVAL to ACTIVE.
        Must be validated against business rule:
        'A plot MUST NOT have more than one active lease at the same time.'
        """
        if self.status != LeaseStatus.PENDING_PAYMENT_OR_APPROVAL:
            raise ValueError(f"Cannot activate lease from status {self.status}")
            
        for lease in existing_leases:
            if lease.id != self.id and lease.status == LeaseStatus.ACTIVE:
                raise ValueError(f"Plot {self.plot_id} already has an active lease.")
                
        self.status = LeaseStatus.ACTIVE
        self.start_time = datetime.now(UTC)

    def complete(self) -> None:
        """Move from ACTIVE to COMPLETED when lease naturally ends successfully."""
        if self.status != LeaseStatus.ACTIVE:
            raise ValueError(f"Cannot complete lease from status {self.status}")
        self.status = LeaseStatus.COMPLETED

    def cancel(self) -> None:
        """Cancel the lease manually (can happen before or during active)."""
        if self.status in [LeaseStatus.COMPLETED, LeaseStatus.EXPIRED, LeaseStatus.TERMINATED]:
            raise ValueError(f"Cannot cancel lease from terminal status {self.status}")
        self.status = LeaseStatus.CANCELLED

    def expire(self) -> None:
        """Mark lease as expired (e.g., failed to pay or ran out of time)."""
        if self.status in [LeaseStatus.COMPLETED, LeaseStatus.CANCELLED, LeaseStatus.TERMINATED]:
            raise ValueError(f"Cannot expire lease from terminal status {self.status}")
        self.status = LeaseStatus.EXPIRED

    def terminate(self) -> None:
        """Terminate the lease abnormally (e.g., policy violation)."""
        if self.status in [LeaseStatus.COMPLETED, LeaseStatus.CANCELLED, LeaseStatus.EXPIRED]:
            raise ValueError(f"Cannot terminate lease from terminal status {self.status}")
        self.status = LeaseStatus.TERMINATED
