from redis.asyncio import Redis, ConnectionPool

class Cache:
    def init(self, url: str):
        self.pool = ConnectionPool.from_url(url)
    
    async def close(self):
        await self.pool.aclose()
    
    async def get_redis(self):
        async with Redis(pool=self.pool) as redis:
            try:
                yield redis
            except Exception as e:
                raise e

cache = Cache()