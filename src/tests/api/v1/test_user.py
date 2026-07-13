from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from httpx import AsyncClient

from src.tests.fake import fake
from src.app.aws import S3Storage
from src.app.core.settings import settings
from src.tests.factories.user import UserFactory

async def test_get_user_me(session: AsyncSession, client: AsyncClient, auth_user):
    UserFactory.set_session(session)
    user = await UserFactory()
    auth_user(user)
    
    res = await client.get("user/me")
    
    result = res.json()
    
    assert res.status_code == 200
    assert result["id"] == user.id
    
async def test_update_user(session: AsyncSession, client: AsyncClient, auth_user):
    new_name = fake.name()
    UserFactory.set_session(session)
    user = await UserFactory()
    auth_user(user)
    
    res = await client.put("user/data/update", json={
        "name": new_name,
    })
    
    result = res.json()
    
    assert res.status_code == 200
    assert result["name"] == new_name

async def test_delete_user(session: AsyncSession, client: AsyncClient, auth_user):
    UserFactory.set_session(session)
    user = await UserFactory()
    auth_user(user)
    
    res = await client.delete("user/delete")
    
    result = res.json()
    
    assert res.status_code == 200
    assert result["success"]
    
async def test_user_avatar_get(session: AsyncSession, client: AsyncClient, storage: S3Storage):
    format = settings.file.base_image_format
    UserFactory.set_session(session)
    user = await UserFactory()
    
    await storage.upload(file="src/tests/test.jpeg", bucket=settings.s3.user_bucket, key=f"avatar-{user.id}-formatted.{format}")
    
    res = await client.get("user/avatar/get", params={
        "id": user.id,
    })

    assert res.status_code == 200
    assert res.content
    
async def test_user_update_avatar(session: AsyncSession, client: AsyncClient, storage: S3Storage, auth_user):
    format = settings.file.base_image_format
    UserFactory.set_session(session)
    user = await UserFactory()
    auth_user(user)
    
    files = {"image": ("test.jpeg", open("src/tests/test.jpeg", "rb"), "image/jpeg")}
    res = await client.put("user/avatar/update", files=files)
    result = res.json()
    
    content = await storage.get(bucket=settings.s3.user_bucket, key=f"avatar-{user.id}-formatted.{format}")
    
    assert res.status_code == 200
    assert result["success"]
    assert content
    
async def test_user_enable_2fa(session: AsyncSession, client: AsyncClient, auth_user):
    UserFactory.set_session(session)
    user = await UserFactory(type_2fa=None)
    auth_user(user)
    
    res = await client.post("user/2fa/enable", json={"type": "email"})
    
    result = res.json()
    
    assert res.status_code == 200
    assert result["success"]

async def test_user_disable_2fa(session: AsyncSession, client: AsyncClient, auth_user):
    UserFactory.set_session(session)
    user = await UserFactory(type_2fa="email")
    auth_user(user)
    
    res = await client.post("user/2fa/disable")
    
    result = res.json()
    
    assert res.status_code == 200
    assert result["success"]