from typing import Literal
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.base import BaseCRUD
from src.app.models.chat import Chat

class ChatCrud(BaseCRUD):
    def __init__(self):
        super().__init__(Chat)
        
    async def add(
        self, session: AsyncSession,
        type: Literal["direct", "group"],
        name: str | None = None,
        description: str | None = None
    ) -> Chat:
        return await super().add(session, type=type, name=name, description=description)
    
chat_crud = ChatCrud()