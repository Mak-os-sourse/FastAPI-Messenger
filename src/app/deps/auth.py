from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError

from src.app.exc.auth import InvalidToken
from src.app.services.security import token
from src.app.crud.user import user_crud
from src.app.core.db import db

security = HTTPBearer()

async def auth_user(
    session: AsyncSession = Depends(db.get_session),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        data = token.decode(credentials.credentials)
        
        if data:
            return await user_crud.get_one(session, id=data["id"])
        else:
            raise InvalidToken()
    except PyJWTError:
        raise InvalidToken()