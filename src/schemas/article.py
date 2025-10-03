from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ArticleCreate(BaseModel):
    title: str
    description: str
    body: str
    tag_list: List[str] = Field(default_factory=list)


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None
    tag_list: Optional[List[str]] = Field(default_factory=list)


class ArticleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    body: str
    tag_list: List[str] = Field(default_factory=list)
    author_id: int

