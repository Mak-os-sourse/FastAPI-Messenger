from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories.user import UserFactory


async def test_create_chat_direct(session: AsyncSession, client: AsyncClient, auth_user):
    user = await UserFactory()
    companion = await UserFactory()
    auth_user(user)
    
    res = await client.post(
        "/chat/direct/create",
        json={
            "companion_id": companion.id,
        }
    )
    
    result = res.json()
    
    assert res.status_code == 200
    assert result["user_id_one"] == user.id
    assert result["user_id_two"] == companion.id