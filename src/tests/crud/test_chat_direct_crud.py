from app.crud.chat_direct import chat_direct_crud
from app.crud.object import ObjectSession
from app.models.chat_direct import ChatDirect
from tests.factories.chat_direct import ChatDirectFactory


async def test_add_if_not_exists_chat(object_session: ObjectSession):
    chat = await chat_direct_crud.add_if_not_exists(object_session, user_id_one=1, user_id_two=2)

    data = await object_session.db.get(ChatDirect, chat.id)

    assert chat.id == data.id
    assert await object_session.redis.keys()


async def test_delete_by_user_id(object_session: ObjectSession):
    chat = await ChatDirectFactory.create(user_id_one=1, user_id_two=2)
    await chat_direct_crud.cache_crud.add(object_session.redis, chat.model_dump())

    await chat_direct_crud.delete_by_user_id(object_session, id=chat.id, user_id=chat.user_id_one)

    data = await object_session.db.get(ChatDirect, chat.id)

    assert not data
    assert not await object_session.redis.keys()
