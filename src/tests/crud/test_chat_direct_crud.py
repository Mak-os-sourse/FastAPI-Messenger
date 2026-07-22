from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.chat_direct import ChatDirect
from src.app.crud.chat_direct import chat_direct_crud

async def test_add_if_not_exists_chat(session: AsyncSession):
    chat = await chat_direct_crud.add_if_not_exists(session, user_id_one=1, user_id_two=2)
    
    data = await session.get(ChatDirect, chat.id)
    
    assert chat.id == data.id