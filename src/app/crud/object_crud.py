from collections.abc import AsyncGenerator, Sequence
from contextlib import asynccontextmanager
from typing import Any

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base import Base
from app.crud.base import BaseCRUD
from app.crud.cache_crud import CacheCrud


class ObjectCrud[T: Base]:
    def __init__(self, model: type[T], prefix: str, keys: Sequence[str]):
        self.db_crud: BaseCRUD[T] = BaseCRUD(model)
        self.cache_crud: CacheCrud = CacheCrud()
        self.prefix: str = self.prefix
        self.keys: Sequence[str] = keys

        if self.prefix and self.prefix[-1] == ":":
            self.prefix[:-1]
        for key in self.keys:
            if getattr(model, key) is None:
                raise ValueError("Such a key is not in the model")

    @asynccontextmanager
    async def bind(self, session: AsyncSession, redis: Redis) -> AsyncGenerator[None]:
        self.session = session
        self.redis = redis
        yield
        del self.session
        del self.redis

    async def add(self, **kargs: Any) -> T:
        result = await self.db_crud.add(self.session, **kargs)
        data = result.model_dump()
        await self.cache_crud.add(self.redis, self._get_key(data), data)
        return result

    async def get(self) -> None: ...

    async def get_all(self) -> None: ...

    async def delete(self) -> None: ...

    async def update(self) -> None: ...

    def _get_key(self, data: dict[Any, Any]) -> str:
        result = self.prefix
        for key in data:
            result += f":{data[key]}:{key}"
        return result
