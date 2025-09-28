from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0001_create_core_tables"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("username", sa.String(), nullable=False, index=True),
        sa.Column("email", sa.String(), nullable=False, unique=True, index=True),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("image_url", sa.String(), nullable=True),
    )

    op.create_table(
        "articles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("tag_list", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    )
    op.create_index("ix_articles_author_id", "articles", ["author_id"])

    op.create_table(
        "comments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("article_id", sa.Integer(), sa.ForeignKey("articles.id", ondelete="CASCADE"), nullable=False),
    )
    op.create_index("ix_comments_article_id", "comments", ["article_id"])
    op.create_index("ix_comments_author_id", "comments", ["author_id"])


def downgrade() -> None:
    op.drop_index("ix_comments_author_id", table_name="comments")
    op.drop_index("ix_comments_article_id", table_name="comments")
    op.drop_table("comments")

    op.drop_index("ix_articles_author_id", table_name="articles")
    op.drop_table("articles")

    op.drop_table("users")
