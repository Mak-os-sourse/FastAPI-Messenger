from sqlalchemy.ext.asyncio import AsyncSession

from app.websocket.tools import WSRouter, WSDpends
from app.schemas.websocket import NewMessege
from app.crud.messege import messege_crud
from app.deps.auth import ws_auth_user
from app.models.user import User
from app.core.db import db

router = WSRouter()

@router.router("NewMessege")
async def new_messege(
    data: NewMessege,
    user: User = WSDpends(ws_auth_user),
    session: AsyncSession = WSDpends(db.get_session)
):
    await messege_crud.add(session, chat_id=data.chat_id, user_id=user.id, content=data.content)