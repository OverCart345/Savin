from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    body: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"))

    author: Mapped["User"] = relationship(back_populates="comments")
    article: Mapped["Article"] = relationship(back_populates="comments")
