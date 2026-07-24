from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from src.app.crud.chat_relationships import chat_relationships_crud
from src.tests.factories.chat_relationships import ChatRelationshipsFactory
from src.tests.factories.invitation import InvitationFactory
from src.tests.factories.chat_group import ChatGroupFactory
from src.tests.factories.user import UserFactory
from src.app.models.chat_group import ChatGroup
from src.app.core.settings import settings
from src.app.aws import S3Storage
from src.tests.fake import fake

async def test_create_chat_group(session: AsyncSession, client: AsyncClient, auth_user):
    user = await UserFactory.create()
    auth_user(user)
    
    res = await client.post(
        "/chat/group/create",
        json={
            "name": fake.name(),
            "type": "public",
            "admin_only": False
        }
    )
    
    result = res.json()
    
    data = await chat_relationships_crud.get_one(session, user_id=user.id, chat_id=result["id"])
    
    assert res.status_code == 200
    assert result["type"] == "public"
    assert data is not None
    
async def test_update_chat_group(client: AsyncClient, auth_user):
    new_name = fake.name()
    chat = await ChatRelationshipsFactory.create(is_admin=True)
    auth_user(chat.user)

    res = await client.put(
        "/chat/group/update",
        json={"name": new_name},
        params={"chat_id" : chat.chat_id}
    )
    
    result = res.json()
    
    assert res.status_code == 200
    assert result["name"] == new_name
    
async def test_update_chat_group_error_not_admin(client: AsyncClient, auth_user):
    new_name = fake.name()
    chat = await ChatRelationshipsFactory.create(is_admin=False)
    auth_user(chat.user)

    res = await client.put(
        "/chat/group/update",
        json={"name": new_name},
        params={"chat_id" : chat.chat_id}
    )
    
    assert res.status_code == 403
    
async def test_chat_avatar_get(client: AsyncClient, storage: S3Storage):
    format = settings.file.base_image_format
    user = await UserFactory.create()
    
    await storage.upload(file="src/tests/test.jpeg", bucket=settings.s3.user_bucket, key=f"avatar-{user.id}.{format}")
    
    res = await client.get("/chat/group/avatar/get", params={
        "id": user.id,
    })

    assert res.status_code == 200
    assert res.content
    
async def test_chat_update_avatar(client: AsyncClient, storage: S3Storage, auth_user):
    format = settings.file.base_image_format
    chat = await ChatRelationshipsFactory.create(is_admin=True)
    auth_user(chat.user)
    
    files = {"image": ("test.jpeg", open("src/tests/test.jpeg", "rb"), "image/jpeg")}
    res = await client.put("/chat/group/avatar/update", files=files, params={"chat_id": chat.chat_id})
    result = res.json()
    
    content = await storage.get(bucket=settings.s3.chat_bucket, key=f"avatar-{chat.chat_id}-formatted.{format}")
    
    assert res.status_code == 200
    assert result["success"]
    assert content

async def test_delete_chat_group(session: AsyncSession, client: AsyncClient, auth_user):
    chat = await ChatRelationshipsFactory.create(is_admin=True)
    auth_user(chat.user)

    res = await client.delete(
        "/chat/group/delete",
        params={"chat_id" : chat.chat_id}
    )
    
    result = res.json()
    data = await session.get(ChatGroup, chat.chat_id)
    
    assert res.status_code == 200
    assert result["success"]
    assert data is None

async def test_join_public_chat_group(session: AsyncSession, client: AsyncClient, auth_user):
    user = await UserFactory.create()
    chat = await ChatRelationshipsFactory.create(is_admin=True, chat__type="public")
    auth_user(user)

    res = await client.post(
        "/chat/group/join",
        json={"chat_id": chat.chat_id}
    )
    
    result = res.json()
    
    data = await chat_relationships_crud.get_one(session, user_id=user.id)
    
    assert res.status_code == 200
    assert result["success"]
    assert data is not None
    
async def test_join_private_chat_group(session: AsyncSession, client: AsyncClient, auth_user):
    user = await UserFactory.create()
    chat = await ChatRelationshipsFactory.create(is_admin=True, chat__type="private")
    auth_user(user)

    res = await client.post(
        "/chat/group/join",
        json={"chat_id": chat.chat_id}
    )
    
    result = res.json()
    
    data = await chat_relationships_crud.get_one(session, user_id=user.id)
    
    assert res.status_code == 200
    assert result["success"]
    assert data is None

async def test_accept_join_chat_group(session: AsyncSession, client: AsyncClient, auth_user):
    chat = await ChatRelationshipsFactory.create(is_admin=True)
    invitation = await InvitationFactory.create(chat_id=chat.chat_id)
    auth_user(chat.user)

    res = await client.post(
        "/chat/group/accept-join",
        params={"chat_id": chat.chat_id},
        json={
            "invitation_id": invitation.id,
            "is_admin": False
        }
    )
    
    result = res.json()
    
    data = await chat_relationships_crud.get_one(session, user_id=invitation.user_id)
    
    assert res.status_code == 200
    assert result["success"]
    assert data is not None
    
async def test_extended_rights_chat_group(session: AsyncSession, client: AsyncClient, auth_user):
    chat_one = await ChatRelationshipsFactory.create(is_admin=True)
    chat_two = await ChatRelationshipsFactory.create(is_admin=False, chat=chat_one.chat)
    auth_user(chat_one.user)

    res = await client.post(
        "/chat/group/extended-rights",
        params={"chat_id": chat_one.chat_id},
        json={"user_id": chat_two.user_id}
    )
    
    result = res.json()
    
    assert res.status_code == 200
    assert result["success"]
    assert chat_two.is_admin