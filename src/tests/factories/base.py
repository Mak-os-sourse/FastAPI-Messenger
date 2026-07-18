from factory.alchemy import SQLAlchemyModelFactory
from sqlalchemy.ext.asyncio import AsyncSession

class SessionManager:
    session: AsyncSession

_session_manager = SessionManager()

class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session_factory = lambda: _session_manager.session
    
    @classmethod
    async def create(cls, **kwargs):
        instance = super().create(**kwargs)
        session: AsyncSession = cls._meta.sqlalchemy_session
        if session is None:
            raise ValueError("No session provided (use set_session).")
        await session.flush()
        return instance

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        instance = super()._create(model_class, *args, **kwargs)
        return instance