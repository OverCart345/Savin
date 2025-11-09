from typing import Dict, Any
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.security import decode_access_token
from clients.users_client import users_client

security = HTTPBearer(auto_error=True)


async def get_db_session(db: AsyncSession = Depends(get_db)) -> AsyncSession:
    return db


async def get_current_user_id(
    creds: HTTPAuthorizationCredentials = Depends(security),
) -> int:

    token = creds.credentials
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

    return user_id


async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    token = creds.credentials
    
    user_data = await users_client.verify_token(token)
    
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    return user_data

