from typing import Literal
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.base import BaseCRUD
from src.app.models.chat_group import ChatGroup

class ChatCrud(BaseCRUD):
    def __init__(self):
        super().__init__(ChatGroup)
        
    async def add(
        self, session: AsyncSession,
        type: Literal["direct", "group"],
        name: str | None = None,
        description: str | None = None,
        is_public_chat: bool = False,
    ) -> ChatGroup:
        return await super().add(
            session, type=type, name=name,
            description=description,
            is_public_chat=is_public_chat
        )
    
chat_group_crud = ChatCrud()