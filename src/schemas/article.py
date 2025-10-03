from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic import ConfigDict


class ArticleCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str
    description: str
    body: str
    tag_list: Optional[List[str]] = Field(default=None, alias="tagList")


class ArticleUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None
    tag_list: Optional[List[str]] = Field(default=None, alias="tagList")


class ArticleOut(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    id: int
    title: str
    description: str
    body: str
    tag_list: Optional[List[str]] = Field(default=None, alias="tagList")
    author_id: int

