from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0002_add_subscription_key"
down_revision: Union[str, None] = "0001_create_users_table"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("subscription_key", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "subscription_key")
