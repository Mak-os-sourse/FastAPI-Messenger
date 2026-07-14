from sqlalchemy.ext.asyncio import AsyncSession

from src.tests.fake import fake
from src.app.models.chat import Chat
from src.app.crud.chat import chat_crud
from src.tests.factories.chat import ChatFactory

async def test_add_chat(session: AsyncSession):
    chat = await chat_crud.add(
        session,
        name=fake.name(),
        description=fake.text(50),
        type="direct"
    )
    
    result = await session.get(Chat, chat.id)
    
    assert result.model_dump() == chat.model_dump()
    
async def test_get_all_chats(session: AsyncSession):
    ChatFactory.set_session(session)
    chat = await ChatFactory()
    
    result = await chat_crud.get_all(session, id=chat.id)
    
    assert result[0].model_dump() == chat.model_dump()

async def test_get_chat(session: AsyncSession):
    ChatFactory.set_session(session)
    chat = await ChatFactory()
    
    result = await chat_crud.get_one(session, id=chat.id)
    
    assert result.model_dump() == chat.model_dump()

async def test_update_chat(session: AsyncSession):
    old_name = fake.name()
    ChatFactory.set_session(session)
    chat = await ChatFactory()
    
    result = await chat_crud.update(session, id=chat.id, name=fake.name())
    
    assert result.name != old_name
    
async def test_delete_chat(session: AsyncSession):
    ChatFactory.set_session(session)
    chat = await ChatFactory()
    
    result = await chat_crud.delete(session, id=chat.id)
    
    assert result is None