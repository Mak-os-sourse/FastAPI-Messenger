from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.messege import messege_crud
from src.app.websocket.manager import ConnectionManager
from src.app.websocket.dispatcher import dp, WSDpends
from src.app.schemas.websocket import NewMessege
from src.app.core.db import db

@dp.router("NewMessege")
async def new_messege(
    data: NewMessege,
    manager: ConnectionManager,
    session: AsyncSession = WSDpends(db.get_session)
):
    await messege_crud.add(session, chat_id=data.chat_id, user_id=1, content=data.content)