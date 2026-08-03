import json

from redis.asyncio import Redis
from redis.asyncio.client import PubSub

from app.services.notification_messeges import NotificationMesseges


async def test_subscribe(redis: Redis):
    notification = NotificationMesseges()
    await notification.subscribe(redis, user_id=1, channel_ids=[2])
    
    assert isinstance(notification._connections[2], PubSub)
    
async def test_unsubscribe(redis: Redis):
    notification = NotificationMesseges()
    await notification.subscribe(redis, user_id=1, channel_ids=[2])
    
    await notification.unsubscribe(user_id=1, channel_ids=[2])
    
    assert not notification._connections
    
async def test_unsubscribe_all(redis: Redis):
    notification = NotificationMesseges()
    await notification.subscribe(redis, user_id=1, channel_ids=[2])
    
    await notification.unsubscribe_all(channel_ids=[2])
    
    assert not notification._connections
    
async def test_publish(redis: Redis):
    notification = NotificationMesseges()
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"notification:{1}:chat_id")
    
    await notification.send_messege(redis, channel_id=1, data={"success": True})
    
    assert await pubsub.get_message() is not None
    
async def test_get_messege(redis: Redis):
    notification = NotificationMesseges()
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"notification:{1}:chat_id")
    await redis.publish(f"notification:{1}:chat_id", json.dumps({"success": True}))
    
    flag = False
    for _ in range(5):
        data = await notification.get_messege(pubsub)
        flag = data == {"success": True}
        if flag: break
    assert flag
    
async def test_listen(redis: Redis):
    count = 0
    notification = NotificationMesseges()
    
    await notification.subscribe(redis, user_id=1, channel_ids=[2])
    await redis.publish(f"notification:{2}:chat_id", json.dumps({"success": True}))
    
    async for data in notification.listen(user_id=1, sleep=0):
        if data is not None:
            assert data == {"success": True}
            break
        count += 1
        if count > 5:
            assert False