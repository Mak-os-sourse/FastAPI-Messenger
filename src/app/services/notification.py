import asyncio
import json
from abc import ABC, abstractmethod
from collections.abc import AsyncIterable

from redis.asyncio import Redis
from redis.asyncio.client import PubSub

from app.services.notification_cache import NotificationCache


class Notification(ABC):
    def __init__(self, cache: NotificationCache = None):
        self.cache = cache if cache is not None else NotificationCache()
        self._connections: dict[int, PubSub] = {}
    
    @abstractmethod
    async def send_messege(self, redis: Redis, key: str, data: dict) -> None:
        await redis.publish(key, json.dumps(data))
    
    async def listen(self, user_id: int, sleep: float = 0.2) -> AsyncIterable[dict]:
        while True:
            for id in self.cache.get_channels(user_id):
                pubsub = self._connections.get(id)
                if pubsub is None:
                    continue
                    
                data = await self.get_messege(pubsub)
                yield data
                await asyncio.sleep(sleep)
        
    async def get_messege(self, pubsub: PubSub) -> dict | None:
        message = await pubsub.get_message(ignore_subscribe_messages=True)
        if message is None:
            return None
        data = json.loads(message["data"])
        return data
    
    @abstractmethod
    async def subscribe(self, redis: Redis, key: str, user_id: int, channel_id: int) -> None: 
        self.cache.add(user_id, [channel_id])
        if not self._connections.get(id, False):
            pubsub = redis.pubsub()
            await pubsub.subscribe(key)
            self._connections[channel_id] = pubsub
                
    async def unsubscribe(self, user_id: int, channel_ids: list[int]) -> None:
        self.cache.remove(user_id, channel_ids)
        
        for chat_id in channel_ids:
            await self._cloase_connection(chat_id)
            
    async def unsubscribe_all(self, channel_ids: list[int]) -> None:
        self.cache.remove_all(channel_ids)
        
        for chat_id in channel_ids:
            await self._cloase_connection(chat_id)
                
    async def _cloase_connection(self, chat_id: int) -> None:
        if self.cache.get_counter(chat_id) > 0:
            return
        connection = self._connections.pop(chat_id, None)
        if connection is not None:
            await connection.aclose()