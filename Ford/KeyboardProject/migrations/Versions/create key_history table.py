"""create key_history table

Revision ID: 0001
Revises:
Create Date: 2026-07-10

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "KeyHistory",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("key", sa.String(50), nullable=False),
        sa.Column("press_time", sa.DateTime, nullable=False),
        sa.Column("ip_address", sa.String(45), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("KeyHistory")