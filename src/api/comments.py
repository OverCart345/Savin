from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db_session, get_current_user
from repositories.article_repo import ArticleRepository
from repositories.comment_repo import CommentRepository
from services.comment_service import CommentService
from schemas.comment import CommentCreate, CommentOut
from models.user import User

router = APIRouter(prefix="/api", tags=["comments"])


@router.post("/articles/{id}/comments", response_model=CommentOut)
def add_comment(id: int, payload: CommentCreate, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    # ensure article exists
    if not ArticleRepository(db).get_by_id(id):
        raise HTTPException(status_code=404, detail="Article not found")
    service = CommentService(CommentRepository(db))
    comment = service.add(body=payload.body, article_id=id, author_id=current_user.id)
    return CommentOut.model_validate(comment.__dict__, from_attributes=True)


@router.get("/articles/{id}/comments", response_model=List[CommentOut])
def list_comments(id: int, db: Session = Depends(get_db_session)):
    if not ArticleRepository(db).get_by_id(id):
        raise HTTPException(status_code=404, detail="Article not found")
    service = CommentService(CommentRepository(db))
    items = service.list_for_article(id)
    return [CommentOut.model_validate(c.__dict__, from_attributes=True) for c in items]


@router.delete("/articles/{id}/comments/{comment_id}")
def delete_comment(id: int, comment_id: int, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    article = ArticleRepository(db).get_by_id(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    repo = CommentRepository(db)
    comment = repo.get_by_id(comment_id)
    if not comment or comment.article_id != id:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id and article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    CommentService(repo).delete(comment)
    return {"status": "deleted"}

