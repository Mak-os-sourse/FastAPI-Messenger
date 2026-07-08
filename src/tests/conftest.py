import pytest_asyncio
from fastapi.testclient import TestClient

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

@pytest_asyncio.fixture()
async def session():
    async with db.sessionmaker() as session:
        yield session
        await session.rollback()
        
      
        
@pytest_asyncio.fixture()
async def client():
    async def get_session():
        async with db.sessionmaker() as ses:
            yield ses
            await ses.rollback()  
    
    app.dependency_overrides[db.get_session] = get_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()