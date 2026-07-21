from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.chat_relationships_crud import chat_relationships_crud
from src.tests.factories.chat_relationships import ChatRelationshipsFactory

async def test_extended_rights_chat(session: AsyncSession):
    chat = await ChatRelationshipsFactory.create()
    
    await chat_relationships_crud.extended_rights(session, user_id=chat.user_id, chat_id=chat.chat_id)
    
    assert chat.is_admin