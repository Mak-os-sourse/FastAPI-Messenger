from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.base import BaseCRUD
from src.app.models.chat_direct import ChatDirect

class ChatDirectCrud(BaseCRUD):
    def __init__(self):
        super().__init__(ChatDirect)
        
    async def add(self, session: AsyncSession, user_id_one: int, user_id_two: int) -> ChatDirect:
        return await super().add(session, user_id_one=user_id_one, user_id_two=user_id_two)
    
    async def add_if_not_exists(self, session: AsyncSession, user_id_one: int, user_id_two: int) -> ChatDirect:
        stmt = insert(self.model).values(user_id_one=user_id_one, user_id_two=user_id_two).returning(self.model)
        stmt.on_conflict_do_nothing(index_elements=["user_id_one", "user_id_two"])
        data = await session.scalars(stmt)
        await session.flush()
        return data.one_or_none()

chat_direct_crud = ChatDirectCrud()