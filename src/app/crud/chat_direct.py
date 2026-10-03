from sqlalchemy import or_
from sqlalchemy.dialects.postgresql import insert

from app.crud.object import ObjectCrud, ObjectSession
from app.models.chat_direct import ChatDirect


class ChatDirectCrud(ObjectCrud[ChatDirect]):
    def __init__(self) -> None:
        super().__init__(ChatDirect)

    async def add(self, session: ObjectSession, user_id_one: int, user_id_two: int) -> ChatDirect:
        return await super().add(session, user_id_one=user_id_one, user_id_two=user_id_two)

    async def add_if_not_exists(
        self,
        session: ObjectSession,
        user_id_one: int,
        user_id_two: int,
    ) -> ChatDirect | None:
        stmt = (
            insert(self.model)
            .values(user_id_one=user_id_one, user_id_two=user_id_two)
            .on_conflict_do_nothing(constraint="unique_user_ids")
            .returning(self.model)
        )
        data = await session.db.scalars(stmt)
        await session.db.flush()
        result = data.one_or_none()
        if result:
            await self.cache_crud.add(session.redis, result.model_dump())
        return result

    async def delete_by_user_id(self, session: ObjectSession, id: int, user_id: int) -> None:
        await chat_direct_crud.db_crud.delete(
            session.db,
            id=id,
            whereclause=[
                or_(
                    ChatDirect.user_id_one == user_id,
                    ChatDirect.user_id_two == user_id,
                ),
            ],
        )
        await chat_direct_crud.cache_crud.pattern_delete(session.redis, user_id=user_id)


chat_direct_crud = ChatDirectCrud()
