from typing import Literal
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.base import BaseCRUD
from src.app.models.chat_relationships import ChatRelationships
from src.app.models.chat import Chat

class ChatCrud(BaseCRUD):
    def __init__(self):
        super().__init__(Chat)
        
    async def add(
        self, session: AsyncSession,
        type: Literal["direct", "group"],
        name: str | None = None,
    ) -> Chat:
        return await super().add(session, type=type, name=name)
    
    async def add_user(
        self, session: AsyncSession,
        chat_id: int,
        user_id: int,
        is_admin: bool = False,
    ) -> ChatRelationships:
        chat_relationships = ChatRelationships(
            chat_id=chat_id,
            user_id=user_id,
            is_admin=is_admin,
        )
        session.add(chat_relationships)
        await session.flush()
        return chat_relationships