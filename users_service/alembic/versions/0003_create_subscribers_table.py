from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0003_create_subscribers_table"
down_revision: Union[str, None] = "0002_add_subscription_key"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "subscribers",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("subscriber_id", sa.BigInteger(), nullable=False),
        sa.Column("author_id", sa.BigInteger(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_subscribers_id", "subscribers", ["id"])
    op.create_index("ux_sub", "subscribers", ["subscriber_id", "author_id"], unique=True)


def downgrade() -> None:
    op.drop_index("ux_sub", table_name="subscribers")
    op.drop_index("ix_subscribers_id", table_name="subscribers")
    op.drop_table("subscribers")
