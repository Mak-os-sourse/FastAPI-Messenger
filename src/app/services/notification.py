import json
from redis.asyncio import Redis
from redis.asyncio.client import PubSub

class Notification:
    def __init__(self):
        self._cache_data: dict[int, list[int]] = {}
        self._connections: dict[int, PubSub] = {}
        
    def add_chat_ids(self, user_id: int, chat_ids: list[int]) -> None:
        data = self._cache_data.get(user_id)
        if data is None:
            self._cache_data[user_id] = chat_ids.copy()
            return None
            
        for id in chat_ids:
            self._cache_data[user_id].append(id)
            
    async def add_chat_connections(self, redis: Redis, chat_ids: list[int]) -> None:
        for chat_id in chat_ids:
            if not self._connections.get(chat_id, False):
                pubsub = redis.pubsub()
                await pubsub.subscribe(f"notification:{chat_id}:chat_id")
                self._connections[chat_id] = pubsub
            
    def delete_chat_ids(self, user_id: int, chat_ids: list[int]) -> None:
        connections = self._cache_data.get(user_id)
        if connections is None:
            return None
        
        for chat_id in chat_ids:
            connections.pop(connections.index(chat_id))
    
    async def delete_chat_connection(self, redis: Redis, chat_ids: list[int]) -> None:
        for chat_id in chat_ids:
            pubsub = self._connections.pop(chat_id)
            await pubsub.aclose()

    async def get_all_messege(self, user_id: int) -> dict | None:
        result = []
        ids = self._cache_data.get(user_id)
        if ids is not None:
            return None
        
        for id in ids:
            data = await self.get_messege(self._connections.get(id))
            if data is not None:
                result.append(data)
    
    async def send_messege(self, redis: Redis, chat_id: int, data: dict) -> None:
        await redis.publish(f"notification:{chat_id}:chat_id", json.dumps(data))
        
    async def get_messege(self, pubsub: PubSub) -> dict | None:
        message = pubsub.get_message(ignore_subscribe_messages=True)
        if message is None:
            return None
        data = json.loads(message["data"])
        return data
    
notification = Notification()