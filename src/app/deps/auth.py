from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import PyJWTError

from app.websocket.dispatcher import WSDpends
from app.schemas.auth import WSToken
from app.exc.auth import InvalidToken, WSInvalidToken
from app.services.security import token
from app.crud.user import user_crud
from app.core.db import db

security = HTTPBearer()

async def ws_auth_user(
    data: WSToken,
    session: AsyncSession = WSDpends(db.get_session),
):
    try:
        data = token.decode(data.token)
        
        if data:
            return await user_crud.get_one(session, id=data["id"])
        else:
            raise WSInvalidToken()
    except PyJWTError:
        raise WSInvalidToken()

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