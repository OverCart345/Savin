from typing import List, Optional
from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str
    description: str
    body: str
    tagList: Optional[List[str]] = None


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None
    tagList: Optional[List[str]] = None


class ArticleOut(BaseModel):
    id: int
    title: str
    description: str
    body: str
    tagList: Optional[List[str]] = None
    author_id: int

