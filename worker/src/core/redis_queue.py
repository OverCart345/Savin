import json
import redis.asyncio as redis

from core.config import settings


class RedisQueue:
    
    def __init__(self):
        self.redis_url = settings.redis_url
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
    
    async def dequeue_notification(self, timeout: int = 0):

        if not self._client:
            await self.connect()
        
        result = await self._client.brpop("notifications_queue", timeout=timeout)
        
        if result:
            _, task_json = result
            return json.loads(task_json)
        
        return None
