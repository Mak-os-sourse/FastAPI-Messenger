import json
from collections import defaultdict

from redis.asyncio import Redis
from redis.asyncio.client import PubSub


class Notification:
    def __init__(self):
        self._cache_user_data: dict[int, set[int]] = {}
        self._cache_chat_data: dict[int, set[int]] = {}
        self._connections: dict[int, PubSub] = {}
        self._count_connections:  dict[int, int] = defaultdict(int)
        
    async def subscribe(self, redis: Redis, user_id: int, chat_ids: list[int]) -> None:
        user_data = self._cache_user_data.setdefault(user_id, set())
            
        for id in chat_ids:
            if not self._connections.get(id, False):
                pubsub = redis.pubsub()
                await pubsub.subscribe(f"notification:{id}:chat_id")
                self._connections[id] = pubsub
                
            user_data.add(id)
            self._count_connections[id] += 1
            self._cache_chat_data.setdefault(id, set()).add(user_id)
            
    async def unsubscribe(self, user_id: int, chat_ids: list[int]) -> None:
        cache = self._cache_user_data.get(user_id)
        if cache is None:
            return
        
        for chat_id in chat_ids:
            cache.discard(chat_id)
            self._count_connections[chat_id] -= 1
            await self._cloase_connection(chat_id)
                
    async def unsubscribe_all(self, chat_ids: list[int]) -> None:
        for chat_id in chat_ids:
            data = self._cache_chat_data.pop(chat_id, None)
            if data is None:
                continue
            for user in data:
                self._cache_user_data[user].discard(chat_id)
                self._count_connections[chat_id] -= 1
                
                await self._cloase_connection(chat_id)

    async def get_all_messege(self, user_id: int) -> list | None:
        result = []
        ids = self._cache_user_data.get(user_id)
        if ids is None:
            return None
        
        for id in ids:
            pubsub = self._connections.get(id)
            if pubsub is None:
                continue
            if self._count_connections.get(id, 0) <= 0:
                return None
                
            data = await self.get_messege(pubsub)
            if data is not None:
                result.append(data)
        return result
    
    async def send_messege(self, redis: Redis, chat_id: int, data: dict) -> None:
        await redis.publish(f"notification:{chat_id}:chat_id", json.dumps(data))
        
    async def get_messege(self, pubsub: PubSub) -> dict | None:
        message = pubsub.get_message(ignore_subscribe_messages=True)
        if message is None:
            return None
        data = json.loads(message["data"])
        return data
    
    async def _cloase_connection(self, chat_id: int) -> None:
        if self._count_connections.get(chat_id, 0) != 0:
            return
        connection = self._connections[chat_id]
        if connection is not None:
            await connection.aclose()
    
notification = Notification()