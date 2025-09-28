from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db_session, get_current_user
from core.security import create_access_token
from repositories.user_repo import UserRepository
from schemas.auth import TokenOut
from schemas.user import UserCreate, UserLogin, UserOut, UserUpdate
from services.user_service import UserService
from models.user import User

router = APIRouter(prefix="/api", tags=["users"])


def _make_service(db: Session) -> UserService:
    return UserService(UserRepository(db))


def _build_response(user: User) -> dict:
    token = create_access_token(str(user.id))
    return {
        "user": UserOut.model_validate(user.__dict__, from_attributes=True),
        "token": TokenOut(access_token=token),
    }


@router.post("/users")
def register_user(payload: UserCreate, db: Session = Depends(get_db_session)):
    service = _make_service(db)
    try:
        user = service.register(
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
def login_user(payload: UserLogin, db: Session = Depends(get_db_session)):
    service = _make_service(db)
    try:
        token = service.authenticate(payload.email, payload.password)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    user = UserRepository(db).get_by_email(payload.email)
    return {
        "user": UserOut.model_validate(user.__dict__, from_attributes=True),
        "token": TokenOut(access_token=token),
    }


@router.get("/user")
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return _build_response(current_user)


@router.put("/user")
def update_user(
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
):
    service = _make_service(db)
    user = service.update_profile(
        current_user,
        email=payload.email,
        username=payload.username,
        password=payload.password,
        bio=payload.bio,
        image_url=payload.image_url,
    )
    return _build_response(user)
