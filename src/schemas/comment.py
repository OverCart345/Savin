from pydantic import BaseModel


class CommentCreate(BaseModel):
    body: str


class CommentOut(BaseModel):
    id: int
    body: str
    author_id: int
    article_id: int

