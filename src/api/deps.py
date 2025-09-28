from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import decode_access_token
from models.user import User
from repositories.user_repo import UserRepository

security = HTTPBearer(auto_error=True)


def get_db_session(db: Session = Depends(get_db)) -> Session:
    return db


def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = creds.credentials
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

