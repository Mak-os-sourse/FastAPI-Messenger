from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from httpx import AsyncClient

from src.tests.fake import fake
from src.app.core.settings import settings
from src.app.services.security import hash_lib
from src.tests.factories.user import UserFactory

async def test_regist_user(client: AsyncClient):
    username, password = fake.user_name(), fake.password()
    res = await client.post("auth/regist", json={
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

async def test_login_user_disable_2fa(session: AsyncSession, client: AsyncClient):
    password = fake.password()
    username = fake.user_name()
    UserFactory.set_session(session)
    await UserFactory(type_2fa=None, username=username, password=hash_lib.hash(password))
    
    res = await client.post("auth/login", json={
        "username": username,
        "password": password,
    })
    
    result = res.json()
    
    assert res.status_code == 200
    assert result["access_token"]
    assert res.cookies.get("token")

async def test_login_user_enable_2fa(session: AsyncSession, client: AsyncClient):
    password = fake.password()
    username = fake.user_name()
    UserFactory.set_session(session)
    user = await UserFactory(type_2fa="email", username=username, password=hash_lib.hash(password))
    
    res = await client.post("auth/login", json={
        "username": username,
        "password": password,
    })
    
    result = res.json()
    
    assert res.status_code == 200
    assert result["user_id"] == user.id
    assert result["access_token"] is None
    assert result["type_2fa"] is not None
    
async def test_verify_gen_code(redis: Redis, session: AsyncSession, client: AsyncClient):
    UserFactory.set_session(session)
    user = await UserFactory()
    
    res = await client.post("auth/verify-code/gen", json={
        "user_id": user.id,
    })

    result = res.json()

    assert res.status_code == 200
    assert result["send_code"]
    assert await redis.keys()
    
async def test_verify_code(redis: Redis, session: AsyncSession, client: AsyncClient):
    UserFactory.set_session(session)
    user = await UserFactory()
    
    code = 357_659
    key = f"{settings.redis.namespace}:verify-code:user:{user.id}:id"
    await redis.set(key, code)
    
    res = await client.post("auth/verify-code/verify", json={
        "user_id": user.id,
        'verify_code': {"code": code},
    })

    result = res.json()
    
    assert res.status_code == 200
    assert result["access_token"]
    assert res.cookies.get("token")
