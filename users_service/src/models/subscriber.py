from datetime import datetime

from sqlalchemy import BigInteger, Index
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Subscriber(Base):
    __tablename__ = "subscribers"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    subscriber_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    author_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)

    __table_args__ = (
        Index("ux_sub", "subscriber_id", "author_id", unique=True),
    )
