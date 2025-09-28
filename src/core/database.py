from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from types import TracebackType

from core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

from typing import Optional, Type

class UnitOfWork:
    def __init__(self) -> None:
        self.session: Session = SessionLocal()

    def __enter__(self) -> Session:
        return self.session

    def __exit__(
            self, 
            exc_type: Optional[Type[BaseException]],
            exc: Optional[BaseException], 
            tb: Optional[TracebackType]
        ) -> None:
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()


def get_db():
    with UnitOfWork() as session:
        yield session
