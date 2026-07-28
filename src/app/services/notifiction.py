import json
from redis.asyncio import Redis

class Notification:
    def __init__(self):
        self.chats: dict[int, list[int]] = {}
        
    def add_chat_ids(self, user_id: int, ids: list[int]):
        self.chats[user_id].extend(ids)
    
    async def get_all_messege(self, redis: Redis, user_id: int) -> dict | None:
        data = self.chats.get(user_id)
        if data is not None:
            for id in data:
                self.get_messege(redis, id)
    
    async def send_messege(self, redis: Redis, chat_id: int, data: dict) -> None:
        await redis.publish(f"notification:{chat_id}:chat_id", json.dumps(data))
        
    async def get_messege(self, redis: Redis, chat_id: int) -> dict | None:
        pubsub = await redis.pubsub()
        await pubsub.subscribe(f"notification:{chat_id}:chat_id")
        for message in pubsub.listen():
            if message["type"] == "messege":
                data = json.loads(message["data"])
                return data