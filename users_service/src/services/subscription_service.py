from datetime import datetime

from models.subscriber import Subscriber
from repositories.subscriber_repo import SubscriberRepository
from repositories.user_repo import UserRepository


class SubscriptionService:
    def __init__(self, subscriber_repo: SubscriberRepository, user_repo: UserRepository) -> None:
        self._subscriber_repo = subscriber_repo
        self._user_repo = user_repo

    async def subscribe(self, subscriber_id: int, author_id: int) -> Subscriber:
        author = await self._user_repo.get_by_id(author_id)
        if not author:
            raise ValueError("Author not found")
        
        existing = await self._subscriber_repo.get_by_subscriber_and_author(
            subscriber_id, author_id
        )
        if existing:
            raise ValueError("Already subscribed")
        
        if subscriber_id == author_id:
            raise ValueError("Cannot subscribe to yourself")
        
        subscription = Subscriber(
            subscriber_id=subscriber_id,
            author_id=author_id,
            created_at=datetime.utcnow()
        )
        return await self._subscriber_repo.create(subscription)

    async def unsubscribe(self, subscriber_id: int, author_id: int) -> None:
        subscription = await self._subscriber_repo.get_by_subscriber_and_author(
            subscriber_id, author_id
        )
        if not subscription:
            raise ValueError("Subscription not found")
        
        await self._subscriber_repo.delete(subscription)
