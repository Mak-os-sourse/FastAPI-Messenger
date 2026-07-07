import pytest_asyncio

from main import app
from src.app.core.settings import settings
from src.app.core.db import db
from src.app.models import *

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup():
    db.init(settings.db.url)
    await db.metadata_create_all()
    yield
    await db.metadata_drop_all()

@pytest_asyncio.fixture(autouse=True)
async def session():
    async with db.sessionmaker() as session:
        app.dependency_overrides[db.get_session] = session
        yield session
        await session.rollback()
        app.dependency_overrides.clear()