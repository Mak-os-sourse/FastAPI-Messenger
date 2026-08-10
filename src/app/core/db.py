from collections.abc import AsyncGenerator
from typing import Any, cast

from sqlalchemy import Pool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.base import Base


class DBConnection:
    def __init__(self) -> None:
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = None

    def init(self, url: str, pool: Pool | None = None) -> None:
        self._engine = create_async_engine(url, pool=pool)
        self._sessionmaker = async_sessionmaker(self.engine)

    @property
    def engine(self) -> AsyncEngine:
        return cast("AsyncEngine", self._check_init(self._engine))

    @property
    def sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        return cast("async_sessionmaker[AsyncSession]", self._check_init(self._sessionmaker))

    def _check_init(self, value: Any) -> Any:
        if value is not None:
            return value
        raise ValueError("The object DB is not initialized, use init(...)")


class DB(DBConnection):
    def __init__(self) -> None:
        super().__init__()

    async def get_session(self) -> AsyncGenerator[AsyncSession]:
        async with self.sessionmaker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e

    async def metadata_create_all(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def metadata_drop_all(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


db = DB()
