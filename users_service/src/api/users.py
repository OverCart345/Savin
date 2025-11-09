from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps import get_db_session, get_current_user
from core.security import create_access_token
from repositories.user_repo import UserRepository
from schemas.auth import TokenOut
from schemas.user import UserCreate, UserLogin, UserOut, UserUpdate
from services.user_service import UserService
from models.user import User

router = APIRouter(prefix="/api", tags=["users"])


def _make_service(db: AsyncSession) -> UserService:
    return UserService(UserRepository(db))


def _build_response(user: User) -> dict:
    token = create_access_token(str(user.id))
    return {
        "user": UserOut.model_validate(user.__dict__, from_attributes=True),
        "token": TokenOut(access_token=token),
    }


@router.post("/users")
async def register_user(payload: UserCreate, db: AsyncSession = Depends(get_db_session)):
    service = _make_service(db)
    try:
        user = await service.register(
            email=payload.email,
            username=payload.username,
            password=payload.password,
            bio=payload.bio,
            image_url=payload.image_url,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return _build_response(user)


@router.post("/users/login")
async def login_user(payload: UserLogin, db: AsyncSession = Depends(get_db_session)):
    service = _make_service(db)
    try:
        token = await service.authenticate(payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    user = await UserRepository(db).get_by_email(payload.email)
    return {
        "user": UserOut.model_validate(user.__dict__, from_attributes=True),
        "token": TokenOut(access_token=token),
    }


@router.get("/user")
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return _build_response(current_user)


@router.put("/user")
async def update_user(
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db_session),
):
    service = _make_service(db)
    user = await service.update_profile(
        current_user,
        email=payload.email,
        username=payload.username,
        password=payload.password,
        bio=payload.bio,
        image_url=payload.image_url,
    )
    return _build_response(user)

@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    user = await UserRepository(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut.model_validate(user.__dict__, from_attributes=True)
