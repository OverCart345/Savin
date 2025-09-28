from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.article import Article


class ArticleRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, article_id: int) -> Optional[Article]:
        return self.db.get(Article, article_id)

    def list(self, limit: int = 20, offset: int = 0) -> List[Article]:
        stmt = select(Article).limit(limit).offset(offset)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, article: Article) -> Article:
        self.db.add(article)
        self.db.flush()
        return article

    def update(self, article: Article) -> Article:
        self.db.flush()
        return article

    def delete(self, article: Article) -> None:
        self.db.delete(article)
