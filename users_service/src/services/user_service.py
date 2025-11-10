from typing import Optional

from core.security import hash_password, verify_password, create_access_token
from models.user import User
from repositories.user_repo import UserRepository


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def register(self, email: str, username: str, password: str, bio: Optional[str] = None, image_url: Optional[str] = None) -> User:
        if await self._repo.get_by_email(email):
            raise ValueError("email already registered")
        user = User(email=email, username=username, password_hash=hash_password(password), bio=bio, image_url=image_url)
        return await self._repo.create(user)

    async def authenticate(self, email: str, password: str) -> str:
        user = await self._repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("invalid credentials")
        return create_access_token(str(user.id))

    async def update_profile(
        self,
        user: User,
        email: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        bio: Optional[str] = None,
        image_url: Optional[str] = None,
        subscription_key: Optional[str] = None,
    ) -> User:
        if email is not None:
            user.email = email
        if username is not None:
            user.username = username
        if password is not None:
            user.password_hash = hash_password(password)
        if bio is not None:
            user.bio = bio
        if image_url is not None:
            user.image_url = image_url
        if subscription_key is not None:
            user.subscription_key = subscription_key
        await self._repo.update(user)
        return user
