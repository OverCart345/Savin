from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    bio: str | None = None
    image_url: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None
    bio: str | None = None
    image_url: str | None = None
    subscription_key: str | None = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    bio: str | None
    image_url: str | None
    subscription_key: str | None = None
