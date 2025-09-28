from typing import List

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text)
    body: Mapped[str] = mapped_column(Text)
    tag_list: Mapped[List[str] | None] = mapped_column(ARRAY(String), nullable=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    author: Mapped["User"] = relationship(back_populates="articles")
    comments: Mapped[List["Comment"]] = relationship(back_populates="article", cascade="all, delete-orphan")
