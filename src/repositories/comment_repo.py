from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.comment import Comment


class CommentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, comment_id: int) -> Optional[Comment]:
        return self.db.get(Comment, comment_id)

    def list_by_article(self, article_id: int) -> List[Comment]:
        stmt = select(Comment).where(Comment.article_id == article_id)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, comment: Comment) -> Comment:
        self.db.add(comment)
        self.db.flush()
        return comment

    def delete(self, comment: Comment) -> None:
        self.db.delete(comment)
