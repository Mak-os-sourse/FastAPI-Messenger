import json, asyncio

from redis.asyncio import Redis
from typing import AsyncIterable
from redis.asyncio.client import PubSub

from app.services.cache_user_chat import cache_chat_user, CacheChatUser

class Notification:
    def __init__(self, cache: CacheChatUser):
        self.cache = cache
        self._connections: dict[int, PubSub] = {}
        
    async def subscribe(self, redis: Redis, user_id: int, chat_ids: list[int]) -> None: 
        self.cache.add(user_id, chat_ids)
        for id in chat_ids:
            if not self._connections.get(id, False):
                pubsub = redis.pubsub()
                await pubsub.subscribe(f"notification:{id}:chat_id")
                self._connections[id] = pubsub
                
    async def unsubscribe(self, user_id: int, chat_ids: list[int]) -> None:
        self.cache.remove(user_id, chat_ids)
        
        for chat_id in chat_ids:
            await self._cloase_connection(chat_id)
            
    async def unsubscribe_all(self, chat_ids: list[int]) -> None:
        self.cache.remove_all(chat_ids)
        
        for chat_id in chat_ids:
            await self._cloase_connection(chat_id)

    async def get_all_messege(self, user_id: int) -> AsyncIterable[dict]:
        while True:
            for id in self.cache._cache_chat_data[user_id]:
                pubsub = self._connections.get(id)
                if pubsub is None:
                    continue
                    
                data = await self.get_messege(pubsub)
                if data is not None:
                    yield data 
    
    async def send_messege(self, redis: Redis, chat_id: int, data: dict) -> None:
        await redis.publish(f"notification:{chat_id}:chat_id", json.dumps(data))
        
    async def get_messege(self, pubsub: PubSub) -> dict | None:
        message = await pubsub.get_message(ignore_subscribe_messages=True)
        if message is None:
            return None
        data = json.loads(message["data"])
        return data
    
    async def _cloase_connection(self, chat_id: int) -> None:
        if self.cache.get_counter(chat_id) > 0:
            return
        connection = self._connections.pop(chat_id, None)
        if connection is not None:
            await connection.aclose()
    
notification = Notification(cache_chat_user)