from typing import List

from sqlalchemy.orm import Session

from models.comment import Comment
from repositories.comment_repo import CommentRepository


class CommentService:
    def __init__(self, repo: CommentRepository) -> None:
        self._repo = repo

    def list_for_article(self, article_id: int) -> List[Comment]:
        return self._repo.list_by_article(article_id)

    def add(self, body: str, article_id: int, author_id: int) -> Comment:
        comment = Comment(body=body, article_id=article_id, author_id=author_id)
        return self._repo.create(comment)

    def delete(self, comment: Comment) -> None:
        self._repo.delete(comment)
