import json
from typing import Any, cast

from redis.asyncio import Redis


class CacheCrud:
    async def add(
        self, redis: Redis, key: str, data: dict[Any, Any], ex: int | None = None
    ) -> None:
        await redis.set(key, json.dumps(data), ex=ex)

    async def get(self, redis: Redis, key: str) -> dict[Any, Any] | None:
        data = await redis.get(key)
        try:
            return cast(dict[Any, Any] | None, json.loads(str(data)))
        except json.JSONDecodeError:
            return None

    async def delete(self, redis: Redis, key: str) -> None:
        await redis.delete(key)

    async def pattern_delete(self, redis: Redis, match: str, cursor: int = 0) -> None:
        data = await redis.scan(match=match)
        for key in data[1]:
            await redis.delete(key)


cache_crud = CacheCrud()
