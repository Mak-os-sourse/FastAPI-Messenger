from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager
from typing import Any

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base import Base
from app.core.cache import cache
from app.core.db import db
from app.crud.base import BaseCRUD
from app.crud.cache_crud import CacheCrud


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

    @asynccontextmanager
    async def bind(
        self,
        session: AsyncSession = Depends(db.get_session),
        redis: Redis = Depends(cache.get_redis),
    ) -> AsyncGenerator[None]:
        self.session = session
        self.redis = redis
        yield
        del self.session
        del self.redis

    async def add(self, **kargs: Any) -> T:
        result = await self.db_crud.add(self.session, **kargs)
        data = result.model_dump()
        await self.cache_crud.add(self.redis, data)
        return result

    async def get(self, **kargs: Any) -> T | None:
        data = await self.get_all(**kargs)
        if data:
            return data[0]
        return None

    async def get_all(self, **kargs: Any) -> Sequence[T]:
        data = await self.cache_crud.get_all(self.redis, **kargs)
        if not data:
            result = await self.db_crud.get_all(self.session, **kargs)
            for model in result:
                await self.add(**model.model_dump())
            return result

        result = []
        for item in data:
            result.append(self.model(**item))
        return result

    async def delete(self, id: int, **kargs: Any) -> None:
        await self.db_crud.delete(self.session, id=id, **kargs)
        await self.cache_crud.pattern_delete(self.redis, **kargs)

    async def update(self, id: int, **kargs: Any) -> T:
        result = await self.db_crud.update(self.session, id=id, **kargs)
        data = result.model_dump()
        await self.cache_crud.add(self.redis, data)
        return result
