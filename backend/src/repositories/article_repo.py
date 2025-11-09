from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.article import Article


class ArticleRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, article_id: int) -> Optional[Article]:
        return await self.db.get(Article, article_id)

    async def list(self, limit: int = 20, offset: int = 0) -> List[Article]:
        stmt = select(Article).limit(limit).offset(offset)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, article: Article) -> Article:
        self.db.add(article)
        await self.db.flush()
        return article

    async def update(self, article: Article) -> Article:
        await self.db.flush()
        return article

    async def delete(self, article: Article) -> None:
        self.db.delete(article)
