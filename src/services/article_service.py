from typing import List, Optional

from sqlalchemy.orm import Session

from models.article import Article
from repositories.article_repo import ArticleRepository


class ArticleService:
    def __init__(self, repo: ArticleRepository) -> None:
        self._repo = repo

    def list(self, limit: int = 20, offset: int = 0) -> List[Article]:
        return self._repo.list(limit=limit, offset=offset)

    def get(self, article_id: int) -> Optional[Article]:
        return self._repo.get_by_id(article_id)

    def create(self, title: str, description: str, body: str, tag_list: Optional[List[str]], author_id: int) -> Article:
        article = Article(title=title, description=description, body=body, tag_list=tag_list, author_id=author_id)
        return self._repo.create(article)

    def update(self, article: Article, title: Optional[str] = None, description: Optional[str] = None, body: Optional[str] = None, tag_list: Optional[List[str]] = None) -> Article:
        if title is not None:
            article.title = title
        if description is not None:
            article.description = description
        if body is not None:
            article.body = body
        if tag_list is not None:
            article.tag_list = tag_list
        return self._repo.update(article)

    def delete(self, article: Article) -> None:
        self._repo.delete(article)
