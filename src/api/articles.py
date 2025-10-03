from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db_session, get_current_user
from repositories.article_repo import ArticleRepository
from services.article_service import ArticleService
from schemas.article import ArticleCreate, ArticleUpdate, ArticleOut
from models.user import User

router = APIRouter(prefix="/api", tags=["articles"])


@router.post("/articles", response_model=ArticleOut)
async def create_article(payload: ArticleCreate, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    service = ArticleService(ArticleRepository(db))
    article = await service.create(
        title=payload.title,
        description=payload.description,
        body=payload.body,
        tag_list=payload.tag_list,
        author_id=current_user.id,
    )
    return ArticleOut.model_validate(article, from_attributes=True)


@router.get("/articles", response_model=List[ArticleOut])
async def list_articles(limit: int = 20, offset: int = 0, db: AsyncSession = Depends(get_db_session)):
    service = ArticleService(ArticleRepository(db))
    items = await service.list(limit=limit, offset=offset)
    return [ArticleOut.model_validate(a, from_attributes=True) for a in items]


@router.get("/articles/{id}", response_model=ArticleOut)
async def get_article(id: int, db: AsyncSession = Depends(get_db_session)):
    service = ArticleService(ArticleRepository(db))
    article = await service.get(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleOut.model_validate(article, from_attributes=True)


@router.put("/articles/{id}", response_model=ArticleOut)
async def update_article(id: int, payload: ArticleUpdate, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    service = ArticleService(ArticleRepository(db))
    article = await service.get(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    article = await service.update(article, title=payload.title, description=payload.description, body=payload.body, tag_list=payload.tag_list)
    return ArticleOut.model_validate(article, from_attributes=True)


@router.delete("/articles/{id}")
async def delete_article(id: int, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    service = ArticleService(ArticleRepository(db))
    article = await service.get(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    if article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    await service.delete(article)
    return {"status": "deleted"}

