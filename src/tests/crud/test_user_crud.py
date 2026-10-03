from app.crud.object import ObjectSession
from app.crud.user import user_crud
from app.models.user import User
from tests.factories.user import UserFactory
from tests.fake import fake


async def test_add_user(object_session: ObjectSession):
    user = await user_crud.add(
        object_session,
        username=fake.user_name(),
        name=fake.name(),
        password=fake.password(),
        email=fake.email(),
        description=fake.text(50),
    )

    result = await object_session.db.get(User, user.id)

    assert result.model_dump() == user.model_dump()


async def test_get_all_users(object_session: ObjectSession):
    user = await UserFactory.create()

    result = await user_crud.get_all(object_session, id=user.id)

    assert result[0].model_dump() == user.model_dump()


async def test_get_user(object_session: ObjectSession):
    user = await UserFactory.create()

    result = await user_crud.get_one(object_session, id=user.id)

    assert result.model_dump() == user.model_dump()


async def test_update_user(object_session: ObjectSession):
    old_name = fake.name()
    user = await UserFactory.create()

    result = await user_crud.update(object_session, id=user.id, name=fake.name())

    assert result.name != old_name


async def test_delete_user(object_session: ObjectSession):
    user = await UserFactory.create()

    await user_crud.delete(object_session, id=user.id)
    result = await object_session.db.get(User, user.id)

    assert result is None
