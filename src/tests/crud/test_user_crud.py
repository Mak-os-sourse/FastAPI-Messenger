from sqlalchemy.ext.asyncio import AsyncSession

from src.tests.fake import fake
from src.app.models.user import User
from src.app.crud.user import user_crud
from src.tests.factories.user import UserFactory

async def test_add_user(session: AsyncSession):
    user = await user_crud.add(
        session,
        username=fake.user_name(),
        name=fake.name(),
        password=fake.password(),
        email=fake.email(),
        description=fake.text(50),
    )
    
    result = await session.get(User, user.id)
    
    assert result.model_dump() == user.model_dump()
    
async def test_get_all_users(session: AsyncSession):
    user = await UserFactory.create()
    
    result = await user_crud.get_all(session, id=user.id)
    
    assert result[0].model_dump() == user.model_dump()

async def test_get_user(session: AsyncSession):
    user = await UserFactory.create()
    
    result = await user_crud.get_one(session, id=user.id)
    
    assert result.model_dump() == user.model_dump()

async def test_update_user(session: AsyncSession):
    old_name = fake.name()
    user = await UserFactory.create()
    
    result = await user_crud.update(session, id=user.id, name=fake.name())
    
    assert result.name != old_name
    
async def test_delete_user(session: AsyncSession):
    user = await UserFactory.create()
    
    result = await user_crud.delete(session, id=user.id)
    
    assert result is None