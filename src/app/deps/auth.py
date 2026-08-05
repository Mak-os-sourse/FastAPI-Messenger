from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import db
from app.crud.user import user_crud
from app.exc.auth import InvalidToken, WSInvalidToken
from app.schemas.auth import WSToken
from app.services.security import token
from app.websocket.tools import WSDpends

security = HTTPBearer()

async def ws_auth_user(
    ws_token: WSToken,
    session: AsyncSession = WSDpends(db.get_session),
):
    try:
        data = token.decode(ws_token.token)
        
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