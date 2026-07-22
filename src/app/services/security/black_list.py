import time
from redis.asyncio import Redis

from src.app.services.security import token
from src.app.core.settings import settings

class BlackList:
    async def set(self, redis: Redis, access: str | None = None, refresh:  str | None = None) -> None:
        now = int(time.time())
        
        if access is not None:
            access_key = f"{settings.redis.namespace}:token-blacklist:{access}:access"
            access_data = token.decode(access)
            await redis.set(access_key, 1, ex=access_data["exp"] - now)
        if refresh is not None:
            refresh_key = f"{settings.redis.namespace}:token-blacklist:{refresh}:refresh"
            refresh_data = token.decode(refresh)
            await redis.set(refresh_key, 1, ex=refresh_data["exp"] - now)
            
    async def get(self, redis: Redis, access: str | None = None, refresh:  str | None = None) -> tuple[bytes | str | None, bytes | str | None]:
        access_data = None
        refresh_data = None
        
        if access is not None:
            access_key = f"{settings.redis.namespace}:token-blacklist:{access}:access"
            access_data = await redis.get(access_key)
        if refresh is not None:
            refresh_key = f"{settings.redis.namespace}:token-blacklist:{refresh}:refresh"
            refresh_data = await redis.get(refresh_key)
            
        return access_data, refresh_data
    
black_list = BlackList()