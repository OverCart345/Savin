import json
import redis.asyncio as redis
from typing import Any, Dict

from core.config import settings


class RedisQueue:

    def __init__(self, redis_url: str = None):
        self.redis_url = redis_url or getattr(settings, 'redis_url', 'redis://redis:6379/0')
        self._client = None
    
    async def connect(self):
        if not self._client:
            self._client = await redis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
        return self._client
    
    async def close(self):
        if self._client:
            await self._client.close()
            self._client = None
    
    async def enqueue_notification(self, author_id: int, post_id: int, post_title: str):
        if not self._client:
            await self.connect()
        
        task = {
            "author_id": author_id,
            "post_id": post_id,
            "post_title": post_title
        }
        
        await self._client.lpush("notifications_queue", json.dumps(task))


redis_queue = RedisQueue()


async def get_redis_queue() -> RedisQueue:
    if not redis_queue._client:
        await redis_queue.connect()
    return redis_queue
