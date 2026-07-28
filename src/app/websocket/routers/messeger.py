from sqlalchemy.ext.asyncio import AsyncSession

from app.websocket.tools import WSRouter, WSDpends
from app.schemas.messege import (
    NewMessege, NewMessegeRequest,
    MessegeResponse
)
from app.crud.messege import messege_crud
from app.deps.auth import ws_auth_user
from app.models.user import User
from app.core.db import db

router = WSRouter()

@router.router("NewMessege", request_model=NewMessegeRequest)
async def new_messege(
    data: NewMessege,
    user: User = WSDpends(ws_auth_user),
    session: AsyncSession = WSDpends(db.get_session)
):
    messege = await messege_crud.add(session=session, chat_id=data.chat_id, user_id=user.id, content=data.content)
    return MessegeResponse(**messege.model_dump())