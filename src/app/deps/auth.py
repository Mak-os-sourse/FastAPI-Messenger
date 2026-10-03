from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError

from app.crud.object import ObjectSession
from app.crud.user import user_crud
from app.exc.auth import InvalidToken, WSInvalidToken
from app.models.user import User
from app.schemas.auth import WSToken
from app.services.security import token
from app.websocket.tools import WSDpends

security = HTTPBearer()


async def ws_auth_user(
    ws_token: WSToken,
    session: ObjectSession = WSDpends(ObjectSession),
) -> User | None:
    try:
        data = token.decode(ws_token.token)

        if data:
            return await user_crud.get_one(session, id=data["id"])
        raise WSInvalidToken()
    except PyJWTError as e:
        raise WSInvalidToken() from e


async def auth_user(
    session: ObjectSession = Depends(),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User | None:
    try:
        data = token.decode(credentials.credentials)

        if data:
            return await user_crud.get_one(session, id=data["id"])
        raise InvalidToken()
    except PyJWTError as e:
        raise InvalidToken() from e
