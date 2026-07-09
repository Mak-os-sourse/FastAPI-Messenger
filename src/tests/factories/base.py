from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy.ext.asyncio import AsyncSession

class BaseFactory(SQLAlchemyModelFactory):
    @classmethod
    def set_session(cls, session: AsyncSession):
        cls._meta.sqlalchemy_session = session
    
    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        instance = super()._create(model_class, *args, **kwargs)
        session: AsyncSession = cls._meta.sqlalchemy_session
        if session is None:
            raise ValueError("No session provided (use set_session).")
        await session.flush()
        return instance