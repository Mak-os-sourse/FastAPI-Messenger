from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.base import BaseCRUD
from src.app.models.messege import Messege

class MessegeCrud(BaseCRUD):
    async def add(
        self, session: AsyncSession,
        chat_id: int,
        user_id: int,
        content: str,
    ) -> Messege:
        return await super().add(
            sesssion=session,
            chat_id=chat_id,
            user_id=user_id,
            content=content,
        )

messege_crud = MessegeCrud()