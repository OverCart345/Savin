from typing import List
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class SubscriberRepository:
    
    def __init__(self, db: AsyncSession):
        self._db = db
    
    async def get_subscribers_with_keys(self, author_id: int) -> List[dict]:
        
        query = text("""
            SELECT s.subscriber_id, u.subscription_key
            FROM subscribers s
            JOIN users u ON u.id = s.subscriber_id
            WHERE s.author_id = :author_id
            AND u.subscription_key IS NOT NULL
        """)
        
        result = await self._db.execute(query, {"author_id": author_id})
        rows = result.fetchall()
        
        return [
            {
                "subscriber_id": row.subscriber_id,
                "subscription_key": row.subscription_key
            }
            for row in rows
        ]
