from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient

from src.tests.fake import fake
from src.app.services.security import hash_lib
from src.tests.factories.user import user_factory

async def test_regist_user(client: TestClient):
    username, password = fake.user_name(), fake.password()
    res = client.post("auth/regist", json={
        "username": username,
        "name": fake.name(),
        "email": fake.email(),
        "description": fake.text(50),
        "password": password,
    })
    
    result = res.json()
    
    assert res.status_code == 200
    assert result["access_token"]
    assert res.cookies.get("token")

async def test_login_user_disable_2fa(session: AsyncSession, client: TestClient):
    password = fake.password()
    username = fake.user_name()
    await user_factory.add(session, type_2fa=None, username=username, password=hash_lib.hash(password))
    await session.commit()
    
    res = client.post("auth/login", json={
        "username": username,
        "password": password,
    })
    
    result = res.json()
    
    assert res.status_code == 200
    assert result["access_token"]
    assert res.cookies.get("token")