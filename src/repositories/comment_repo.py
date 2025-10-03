from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.comment import Comment


class CommentRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, comment_id: int) -> Optional[Comment]:
        return await self.db.get(Comment, comment_id)

    async def list_by_article(self, article_id: int) -> List[Comment]:
        stmt = select(Comment).where(Comment.article_id == article_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, comment: Comment) -> Comment:
        self.db.add(comment)
        await self.db.flush()
        return comment

    async def delete(self, comment: Comment) -> None:
        self.db.delete(comment)
