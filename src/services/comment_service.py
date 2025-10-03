from typing import List

from models.comment import Comment
from repositories.comment_repo import CommentRepository


class CommentService:
    def __init__(self, repo: CommentRepository) -> None:
        self._repo = repo

    async def list_for_article(self, article_id: int) -> List[Comment]:
        return await self._repo.list_by_article(article_id)

    async def add(self, body: str, article_id: int, author_id: int) -> Comment:
        comment = Comment(body=body, article_id=article_id, author_id=author_id)
        return await self._repo.create(comment)

    async def delete(self, comment: Comment) -> None:
        await self._repo.delete(comment)
