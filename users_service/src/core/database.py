from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from types import TracebackType

from core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(settings.database_url, pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

from typing import Optional, Type

class AsyncUnitOfWork:
    def __init__(self) -> None:
        self.session: AsyncSession = AsyncSessionLocal()

    async def __aenter__(self) -> AsyncSession:
        return self.session

    async def __aexit__(
            self, 
            exc_type: Optional[Type[BaseException]],
            exc: Optional[BaseException], 
            tb: Optional[TracebackType]
        ) -> None:
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()


async def get_db():
    async with AsyncUnitOfWork() as session:
        yield session
