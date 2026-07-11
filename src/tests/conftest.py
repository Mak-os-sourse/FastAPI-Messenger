import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis

from main import app
from src.app.core.settings import settings
from src.app.aws import S3Storage, s3, get_storage
from src.app.deps.auth import auth_user as auth_user_deps
from src.app.core.cache import cache
from src.app.core.db import db
from src.app.models import *

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup():
    db.init(settings.db.url)
    cache.init(settings.redis.url)
    await s3.init(settings.s3.url, user=settings.s3.user, password=settings.s3.password)
    await db.metadata_create_all()
    yield
    await db.metadata_drop_all()
    await cache.close()
    await s3.close()

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
async def storage():
    yield S3Storage(s3.client)
  
@pytest_asyncio.fixture()
async def client(session, redis, storage):
    app.dependency_overrides[db.get_session] = lambda: session
    app.dependency_overrides[cache.get_redis] = lambda: redis
    app.dependency_overrides[get_storage] = lambda: storage
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

@pytest_asyncio.fixture()
async def auth_user():
    def func(user: User):
        app.dependency_overrides[auth_user_deps] = lambda: user
    yield func