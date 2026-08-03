from redis.asyncio import Redis

from app.services.notification import Notification


class NotificationMesseges(Notification):
    def __init__(self, cache = None):
        super().__init__(cache)
        
    async def subscribe(self, redis: Redis, user_id: int, channel_ids: list[int]) -> None:
        for channel_id in channel_ids:
            await super().subscribe(redis, key=f"notification:{channel_id}:chat_id", user_id=user_id, channel_id=channel_id)
    
    async def send_messege(self, redis: Redis, channel_id: int, data: dict):
        await super().send_messege(redis, f"notification:{channel_id}:chat_id", data)

notification_messeges = NotificationMesseges()