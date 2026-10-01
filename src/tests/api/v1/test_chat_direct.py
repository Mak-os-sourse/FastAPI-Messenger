from httpx import AsyncClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat_direct import ChatDirect
from tests.factories.chat_direct import ChatDirectFactory
from tests.factories.user import UserFactory


async def test_create_chat_direct(client: AsyncClient, redis: Redis, auth_user):
    user = await UserFactory.create()
    companion = await UserFactory.create()
    auth_user(user)

    res = await client.post(
        "/chat/direct/create",
        json={
            "companion_id": companion.id,
        },
    )

    result = res.json()

    assert res.status_code == 200
    assert result["user_id_one"] == user.id
    assert result["user_id_two"] == companion.id
    assert await redis.keys()


async def test_delete_chat_direct(
    session: AsyncSession, client: AsyncClient, redis: Redis, auth_user
):
    user = await UserFactory.create()
    chat = await ChatDirectFactory.create(user_id_one=user.id, user_id_two=2)
    await redis.set(
        (
            f"chat-relationships:{chat.id}:chat_id"
            f":{user.id}:user_id_one"
            f":{chat.user_id_two}:user_id_two"
        ),
        "",
    )
    auth_user(user)

    res = await client.delete("/chat/direct/delete", params={"chat_id": chat.id})

    result = res.json()
    data = await session.get(ChatDirect, chat.id)

    assert res.status_code == 200
    assert result["success"]
    assert not await redis.keys()
    assert data is None
