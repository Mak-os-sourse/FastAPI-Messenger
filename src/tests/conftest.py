import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis

from main import app
from src.app.core.settings import settings
from src.app.core.db import db
from src.app.core.cache import cache
from src.app.models import *

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup():
    db.init(settings.db.url)
    cache.init(settings.redis.url)
    await db.metadata_create_all()
    yield
    await db.metadata_drop_all()

@pytest_asyncio.fixture()
async def redis():
    async with Redis(connection_pool=cache.pool) as redis:
        yield redis
        await redis.flushall()

@pytest_asyncio.fixture()
async def session():
    async with db.sessionmaker() as session:
        yield session
        await session.rollback()
        
@pytest_asyncio.fixture()
async def client(session, redis):
    app.dependency_overrides[db.get_session] = lambda: session
    app.dependency_overrides[cache.get_redis] = lambda: redis
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()