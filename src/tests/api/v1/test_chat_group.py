from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from src.app.crud.chat_relationships_crud import chat_relationships_crud
from src.tests.factories.chat_relationships import ChatRelationshipsFactory
from src.tests.factories.user import UserFactory
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