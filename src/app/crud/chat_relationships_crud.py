from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.base import BaseCRUD
from src.app.models.chat_relationships import ChatRelationships

class ChatRelationshipsCrud(BaseCRUD):
    async def add(
        self, session: AsyncSession,
        chat_id: int,
        user_id: int,
        is_admin: bool = False,
    ) -> ChatRelationships:
        return await super().add(
            sesssion=session,
            chat_id=chat_id,
            user_id=user_id,
            is_admin=is_admin,
        )

chat_relationships_crud = ChatRelationshipsCrud()