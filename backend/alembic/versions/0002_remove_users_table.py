from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0002_remove_users_table"
down_revision: Union[str, None] = "0001_create_core_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("articles_author_id_fkey", "articles", type_="foreignkey")
    op.drop_constraint("comments_author_id_fkey", "comments", type_="foreignkey")
    op.drop_table("users")


def downgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False, index=True),
        sa.Column("email", sa.String(), nullable=False, unique=True, index=True),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    
    op.create_foreign_key(
        "articles_author_id_fkey",
        "articles",
        "users",
        ["author_id"],
        ["id"],
        ondelete="CASCADE",
    )
    
    op.create_foreign_key(
        "comments_author_id_fkey",
        "comments",
        "users",
        ["author_id"],
        ["id"],
        ondelete="CASCADE",
    )
