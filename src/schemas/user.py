from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    bio: Optional[str] = None
    image_url: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    image_url: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    bio: Optional[str] = None
    image_url: Optional[str] = None

