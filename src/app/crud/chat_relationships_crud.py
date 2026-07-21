from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from src.app.crud.base import BaseCRUD
from src.app.models.chat_relationships import ChatRelationships

class ChatRelationshipsCrud(BaseCRUD):
    def __init__(self):
        super().__init__(ChatRelationships)
    
    async def add(
        self, session: AsyncSession,
        chat_id: int,
        user_id: int,
        is_admin: bool = False,
    ) -> ChatRelationships:
        return await super().add(
            session=session,
            chat_id=chat_id,
            user_id=user_id,
            is_admin=is_admin,
        )
    
    async def extended_rights(self, session: AsyncSession, user_id: int, chat_id: int) -> None:
        stmt = update(ChatRelationships) \
            .where(
                ChatRelationships.user_id == user_id,
                ChatRelationships.chat_id == chat_id
            ) \
            .values(is_admin=True)
        await session.execute(stmt)
        await session.flush()

chat_relationships_crud = ChatRelationshipsCrud()