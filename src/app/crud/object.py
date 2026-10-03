from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base import Base
from app.core.cache import cache
from app.core.db import db
from app.crud.base import BaseCRUD
from app.crud.cache import CacheCrud


@dataclass(slots=True)
class ObjectSession:
    db: AsyncSession = Depends(db.get_session)  # noqa: RUF009
    redis: Redis = Depends(cache.get_redis)  # noqa: RUF009


class ObjectCrud[T: Base]:
    def __init__(self, model: type[T], keys: Sequence[str] | None = None):
        self.model = model
        self.db_crud: BaseCRUD[T] = BaseCRUD(model)
        self.cache_crud: CacheCrud = CacheCrud(model.__tablename__, keys)

        if not keys:
            return
        if "id" not in keys:
            raise ValueError("The id key must be in keys")
        for key in keys:
            if getattr(model, key, None) is None:
                raise ValueError("Such a key is not in the model")

    async def add(self, session: ObjectSession, **kargs: Any) -> T:
        result = await self.db_crud.add(session.db, **kargs)
        data = result.model_dump()
        await self.cache_crud.add(session.redis, data)
        return result

    async def get_one(self, session: ObjectSession, **kargs: Any) -> T | None:
        data = await self.get_all(session, **kargs)
        if data:
            return data[0]
        return None

    async def get_all(self, session: ObjectSession, **kargs: Any) -> Sequence[T]:
        data = await self.cache_crud.get_all(session.redis, **kargs)
        if not data:
            result = await self.db_crud.get_all(session.db, **kargs)
            for model in result:
                await self.cache_crud.add(session.redis, model.model_dump())
            return result

        result = []
        for item in data:
            result.append(self.model(**item))
        return result

    async def delete(self, session: ObjectSession, id: int, **kargs: Any) -> None:
        await self.db_crud.delete(session.db, id=id, **kargs)
        await self.cache_crud.pattern_delete(session.redis, **kargs)

    async def update(self, session: ObjectSession, id: int, **kargs: Any) -> T:
        result = await self.db_crud.update(session.db, id=id, **kargs)
        data = result.model_dump()
        await self.cache_crud.add(session.redis, data)
        return result
