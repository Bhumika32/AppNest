"""add unique_hash to xp_transactions

Revision ID: ae813eebb392
Revises: c222c540e41e
Create Date: 2026-03-30 12:21:48.221458

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ae813eebb392'
down_revision: Union[str, None] = 'c222c540e41e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "xp_transactions",
        sa.Column("unique_hash", sa.String(length=255), nullable=True)
    )

    op.create_index(
        "ix_xp_transactions_unique_hash",
        "xp_transactions",
        ["unique_hash"],
        unique=True
    )


def downgrade() -> None:
    op.drop_index("ix_xp_transactions_unique_hash", table_name="xp_transactions")
    op.drop_column("xp_transactions", "unique_hash")