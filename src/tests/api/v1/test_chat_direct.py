from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from src.tests.factories.user import UserFactory
from src.tests.fake import fake

async def test_create_chat_direct(session: AsyncSession, client: AsyncClient, auth_user):
    UserFactory.set_session(session)
    user = await UserFactory()
    companion = await UserFactory()
    auth_user(user)
    
    res = await client.post(
        "/chat/direct/create",
        json={
            "companion_id": companion.id,
            "name": fake.name()
        }
    )
    
    result = res.json()
    
    assert res.status_code == 200
    assert result["type"] == "direct"