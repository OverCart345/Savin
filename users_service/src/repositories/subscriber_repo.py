from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.subscriber import Subscriber
from models.user import User


class SubscriberRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create(self, subscriber: Subscriber) -> Subscriber:
        self._db.add(subscriber)
        await self._db.commit()
        await self._db.refresh(subscriber)
        return subscriber

    async def get_by_subscriber_and_author(
        self, subscriber_id: int, author_id: int
    ) -> Subscriber | None:
        stmt = select(Subscriber).where(
            Subscriber.subscriber_id == subscriber_id,
            Subscriber.author_id == author_id,
        )
        result = await self._db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_subscribers_by_author(self, author_id: int) -> List[Subscriber]:
        stmt = select(Subscriber).where(Subscriber.author_id == author_id)
        result = await self._db.execute(stmt)
        return list(result.scalars().all())
    
    async def get_subscribers_with_keys(self, author_id: int) -> List[dict]:
        stmt = (
            select(Subscriber.subscriber_id, User.subscription_key)
            .join(User, User.id == Subscriber.subscriber_id)
            .where(Subscriber.author_id == author_id)
            .where(User.subscription_key.isnot(None))
        )
        result = await self._db.execute(stmt)
        return [
            {"subscriber_id": row.subscriber_id, "subscription_key": row.subscription_key}
            for row in result.all()
        ]

    async def delete(self, subscriber: Subscriber) -> None:
        await self._db.delete(subscriber)
        await self._db.commit()
