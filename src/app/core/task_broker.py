import os
from taskiq import InMemoryBroker
from taskiq_redis import RedisStreamBroker

from src.app.core.settings import settings

if os.getenv("TEST") is not None:
    broker = InMemoryBroker(await_inplace=True)
else:
    broker = RedisStreamBroker(settings.redis.url)