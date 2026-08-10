from collections.abc import AsyncGenerator

from redis.asyncio import ConnectionPool, Redis


class CacheConnection:
    def __init__(self) -> None:
        self._pool: ConnectionPool | None = None

    def init(self, url: str) -> None:
        self._pool = ConnectionPool.from_url(url, decode_responses=True)

    @property
    def pool(self) -> ConnectionPool:
        if self._pool is not None:
            return self._pool
        raise ValueError("The object Cache is not initialized, use init(...)")


class Cache(CacheConnection):
    def __init__(self) -> None:
        super().__init__()

    async def close(self) -> None:
        await self.pool.aclose()

    async def get_redis(self) -> AsyncGenerator[Redis]:
        async with Redis(connection_pool=self.pool) as redis:
            try:
                yield redis
            except Exception as e:
                raise e


cache = Cache()
