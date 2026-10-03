import json
from collections.abc import Sequence
from typing import Any

from redis.asyncio import Redis


class CacheCrud:
    def __init__(self, prefix: str, keys: Sequence[str] | None = None):
        self.prefix = prefix
        self.keys = keys

    async def add(self, redis: Redis, data: dict[Any, Any], ex: int | None = None) -> None:
        await redis.set(self._get_key(data), json.dumps(data), ex=ex)

    async def get(self, redis: Redis, **kargs: Any) -> dict[Any, Any] | None:
        data = await self.get_all(redis, **kargs)
        if data:
            return data[0]
        return None

    async def get_all(self, redis: Redis, **kargs: Any) -> list[dict[Any, Any]]:
        result = []
        keys = await redis.scan(match=self._get_match(kargs))
        try:
            for key in keys[1]:
                item = await redis.get(key)
                result.append(json.loads(str(item)))
        except json.JSONDecodeError:
            return []
        return result

    async def delete(self, redis: Redis, **kargs: Any) -> None:
        keys = self._get_match(kargs)
        for key in keys:
            await redis.delete(key)

    async def pattern_delete(self, redis: Redis, cursor: int = 0, **kargs: Any) -> None:
        data = await redis.scan(cursor, match=self._get_match(kargs))
        for key in data[1]:
            await redis.delete(key)

    def _get_key(self, data: dict[Any, Any]) -> str:
        result = self.prefix
        items = self.keys if self.keys else data.keys()
        for key in items:
            result += f":{data[key]}:{key}"
        return result

    def _get_match(self, data: dict[Any, Any]) -> str:
        match = f"{self.prefix}"
        for key, value in data.items():
            match += f"*{value}:{key}*"
        return match
