from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db_session, get_current_user
from repositories.article_repo import ArticleRepository
from services.article_service import ArticleService
from schemas.article import ArticleCreate, ArticleUpdate, ArticleOut
from models.user import User

router = APIRouter(prefix="/api", tags=["articles"])


@router.post("/articles", response_model=ArticleOut)
def create_article(payload: ArticleCreate, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    service = ArticleService(ArticleRepository(db))
    article = service.create(
        title=payload.title,
        description=payload.description,
        body=payload.body,
        tag_list=payload.tagList,
        author_id=current_user.id,
    )
    return ArticleOut.model_validate(article.__dict__, from_attributes=True)


@router.get("/articles", response_model=List[ArticleOut])
def list_articles(limit: int = 20, offset: int = 0, db: Session = Depends(get_db_session)):
    service = ArticleService(ArticleRepository(db))
    items = service.list(limit=limit, offset=offset)
    return [ArticleOut.model_validate(a.__dict__, from_attributes=True) for a in items]


@router.get("/articles/{id}", response_model=ArticleOut)
def get_article(id: int, db: Session = Depends(get_db_session)):
    service = ArticleService(ArticleRepository(db))
    article = service.get(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleOut.model_validate(article.__dict__, from_attributes=True)


@router.put("/articles/{id}", response_model=ArticleOut)
def update_article(id: int, payload: ArticleUpdate, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    service = ArticleService(ArticleRepository(db))
    article = service.get(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    article = service.update(article, title=payload.title, description=payload.description, body=payload.body, tag_list=payload.tagList)
    return ArticleOut.model_validate(article.__dict__, from_attributes=True)


@router.delete("/articles/{id}")
def delete_article(id: int, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    service = ArticleService(ArticleRepository(db))
    article = service.get(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    service.delete(article)
    return {"status": "deleted"}

