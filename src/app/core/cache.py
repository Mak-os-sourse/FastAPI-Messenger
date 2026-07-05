from redis.asyncio import Redis, ConnectionPool

from src.app.core.settings import settings

class Cache:
    def __init__(self, url: str):
        self.pool = ConnectionPool.from_url(url)

    async def get_redis(self):
        redis = Redis(pool=self.pool)
        yield redis
        await redis.aclose()

cache = Cache(settings.redis.url)