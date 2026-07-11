import pyotp
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from httpx import AsyncClient

from src.tests.fake import fake
from src.app.core.settings import settings
from src.app.services.security import hash_lib
from src.tests.factories.user import UserFactory
from src.app.services.security import totp, token

async def test_update_token(session: AsyncSession, client: AsyncClient):
    UserFactory.set_session(session)
    user = await UserFactory()
    access, refresh = token.create_tokens(id=user.id, username=user.username, email=user.email)
    
    res = await client.post(
        "auth/update-token",
        headers={"Authorization": f"Bearer {access}"},
        cookies={"token": refresh},
    )
    
    result = res.json()
    
    assert res.status_code == 200
    assert result["access_token"]
    assert res.cookies.get("token")

async def test_update_token_fail_blacklist(redis: Redis, session: AsyncSession, client: AsyncClient):
    UserFactory.set_session(session)
    user = await UserFactory()
    access, refresh = token.create_tokens(id=user.id, username=user.username, email=user.email)
    access_key = f"{settings.redis.namespace}:token-blacklist:{access}:access"
    await redis.set(access_key, 1)
    
    res = await client.post(
        "auth/update-token",
        headers={"Authorization": f"Bearer {access}"},
        cookies={"token": refresh},
    )
    
    assert res.status_code == 401

async def test_update_token_error_token(session: AsyncSession, client: AsyncClient):
    UserFactory.set_session(session)
    user = await UserFactory()
    _, refresh = token.create_tokens(id=user.id, username=user.username, email=user.email)
    
    res = await client.post(
        "auth/update-token",
        headers={"Authorization": f"Bearer w5a234fa"},
        cookies={"token": refresh},
    )
    
    assert res.status_code == 401

async def test_regist_user_error_user_is_exists(session: AsyncSession, client: AsyncClient):
    UserFactory.set_session(session)
    user = await UserFactory()
    username = user.username
    res = await client.post("auth/regist", json={
        "username": username,
        "name": fake.name(),
        "email": fake.email(),
        "description": fake.text(50),
        "password": fake.password(),
    })
    
    assert res.status_code == 409

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

async def test_login_user_error_user_not_found(client: AsyncClient):
    res = await client.post("auth/login", json={
        "username": fake.user_name(),
        "password": fake.password(),
    })
    
    assert res.status_code == 401

async def test_login_user_error_fail_password(session: AsyncSession, client: AsyncClient):
    password = fake.password()
    username = fake.user_name()
    UserFactory.set_session(session)
    user = await UserFactory(type_2fa="email", username=username, password=hash_lib.hash(password))
    
    res = await client.post("auth/login", json={
        "username": user.username,
        "password": fake.password(),
    })
    
    assert res.status_code == 401

async def test_verify_gen_code(redis: Redis, session: AsyncSession, client: AsyncClient):
    UserFactory.set_session(session)
    user = await UserFactory()
    
    res = await client.post("auth/verify-code/gen", params={
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
    
    res = await client.post(
        "auth/verify-code/verify",
        json={"code": code},
        params={"user_id": user.id}
    )

    result = res.json()
    
    assert res.status_code == 200
    assert result["access_token"]
    assert res.cookies.get("token")
    
async def test_verify_code_error_invalid_code(redis: Redis, session: AsyncSession, client: AsyncClient):
    UserFactory.set_session(session)
    user = await UserFactory()
    
    code = 357_659
    key = f"{settings.redis.namespace}:verify-code:user:{user.id}:id"
    await redis.set(key, code)
    
    res = await client.post(
        "auth/verify-code/verify",
        json={"code": 412_657},
        params={"user_id": user.id}
    )
    
    assert res.status_code == 401

async def test_gen_qecode(session: AsyncSession, client: AsyncClient):
    UserFactory.set_session(session)
    user = await UserFactory(secret_key=totp.gen_secret_key())
    
    res = await client.post(
        "auth/opt/gen-qrcode",
        params={"user_id": user.id}
    )
    
    assert res.status_code == 200
    assert res.content

async def test_gen_qecode_error_not_enable_2fa(session: AsyncSession, client: AsyncClient):
    UserFactory.set_session(session)
    user = await UserFactory()
    
    res = await client.post(
        "auth/opt/gen-qrcode",
        params={"user_id": user.id}
    )
    
    assert res.status_code == 409
    assert res.content

async def test_verify_otp(session: AsyncSession, client: AsyncClient):
    UserFactory.set_session(session)
    user = await UserFactory(secret_key=totp.gen_secret_key())
    code = pyotp.TOTP(user.secret_key).now()
    
    res = await client.post(
        "auth/otp/verify",
        json={"code": code},
        params={"user_id": user.id}
    )
    
    result = res.json()
    
    assert res.status_code == 200
    assert result["access_token"]
    assert res.cookies.get("token")

async def test_logout(redis: Redis, session: AsyncSession, client: AsyncClient):
    UserFactory.set_session(session)
    user = await UserFactory()
    access, refresh = token.create_tokens(id=user.id, username=user.username, email=user.email)
    
    res = await client.post(
        "auth/logout",
        headers={"Authorization": f"Bearer {access}"},
        cookies={"token": refresh},
    )
    
    result = res.json()
    
    assert res.status_code == 200
    assert result["success"]
    assert not res.cookies.get("token")
    assert len(await redis.keys()) == 2