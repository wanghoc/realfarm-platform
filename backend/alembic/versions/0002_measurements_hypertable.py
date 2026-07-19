"""measurements TimescaleDB hypertable

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-20
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "measurements",
        sa.Column("measured_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("message_id", sa.String(64), nullable=False),
        sa.Column("device_id", sa.String(128), nullable=False),
        sa.Column("plot_id", sa.String(64), nullable=True),
        sa.Column("sensor_type", sa.String(32), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("unit", sa.String(32), nullable=False),
        sa.Column("quality", sa.String(16), nullable=False),
        sa.Column("quarantine_reason", sa.String(255), nullable=True),
        sa.Column("signature", sa.String(255), nullable=True),
        sa.Column(
            "ingested_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        # Composite PK includes the partition column: TimescaleDB requires the
        # partitioning column in every unique constraint, and (measured_at, message_id)
        # makes a redelivered message idempotent.
        sa.PrimaryKeyConstraint("measured_at", "message_id"),
    )
    op.create_index("ix_measurements_plot_id", "measurements", ["plot_id"])

    # TimescaleDB: turn measurements into a hypertable partitioned on measured_at.
    # Postgres/Timescale only; SQLite keeps the plain table created above.
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("CREATE EXTENSION IF NOT EXISTS timescaledb")
        op.execute(
            "SELECT create_hypertable('measurements', 'measured_at', "
            "if_not_exists => TRUE, migrate_data => TRUE)"
        )


def downgrade() -> None:
    op.drop_index("ix_measurements_plot_id", table_name="measurements")
    op.drop_table("measurements")
