import json
from redis.asyncio import Redis
from redis.asyncio.client import PubSub

from app.services.notification import Notification, CacheChatUser

async def test_subscribe(redis: Redis):
    notification = Notification(CacheChatUser())
    await notification.subscribe(redis, user_id=1, chat_ids=[2])
    
    assert isinstance(notification._connections[2], PubSub)
    
async def test_unsubscribe(redis: Redis):
    notification = Notification(CacheChatUser())
    await notification.subscribe(redis, user_id=1, chat_ids=[2])
    
    await notification.unsubscribe(user_id=1, chat_ids=[2])
    
    assert not notification._connections
    
async def test_unsubscribe_all(redis: Redis):
    notification = Notification(CacheChatUser())
    await notification.subscribe(redis, user_id=1, chat_ids=[2])
    
    await notification.unsubscribe_all(chat_ids=[2])
    
    assert not notification._connections
    
async def test_publish(redis: Redis):
    notification = Notification(CacheChatUser())
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"notification:{1}:chat_id")
    
    await notification.send_messege(redis, chat_id=1, data={"success": True})
    
    assert await pubsub.get_message() is not None
    
async def test_get_messege(redis: Redis):
    notification = Notification(CacheChatUser())
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"notification:{1}:chat_id")
    await redis.publish(f"notification:{1}:chat_id", json.dumps({"success": True}))
    
    for _ in range(5):
        data = await notification.get_messege(pubsub)
        if data is not None:
            assert data == {"success": True}