from collections.abc import Sequence
from typing import Any

from sqlalchemy import BinaryExpression, ColumnElement, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base import Base


class BaseCRUD[T: Base]:
    def __init__(self, model: type[T]) -> None:
        self.model = model
        self.model_keys = model.__dict__.keys()

    async def add(self, session: AsyncSession, **values: Any) -> T:
        stmt = insert(self.model).values(**values).returning(self.model)
        result = await session.scalars(stmt)
        await session.flush()
        return result.one()

    async def get_all(
        self,
        session: AsyncSession,
        whereclause: Sequence[BinaryExpression[bool] | ColumnElement[bool]] | None = None,
        **equality_where: Any,
    ) -> Sequence[T]:
        data = self.get_where(**equality_where)
        stmt = select(self.model).where(*data, *whereclause or [])
        result = await session.scalars(stmt)
        return result.all()

    async def get_one(
        self,
        session: AsyncSession,
        whereclause: Sequence[BinaryExpression[bool] | ColumnElement[bool]] | None = None,
        **equality_where: Any,
    ) -> T | None:
        result = await self.get_all(session, **equality_where, whereclause=whereclause)
        if result:
            return result[0]
        return None

    async def update(self, session: AsyncSession, id: int, **values: Any) -> T:
        stmt = update(self.model).where(self.model.id == id).values(**values).returning(self.model)
        resutl = await session.scalars(stmt)
        await session.flush()
        return resutl.one()

    async def delete(
        self,
        session: AsyncSession,
        id: int,
        whereclause: Sequence[BinaryExpression[bool] | ColumnElement[bool]] | None = None,
        **equality_where: Any,
    ) -> None:
        data = self.get_where(**equality_where)
        stmt = delete(self.model).where(*data, self.model.id == id, *whereclause or [])
        await session.execute(stmt)
        await session.flush()

    def get_where(self, **data: Any) -> Sequence[BinaryExpression[bool] | ColumnElement[bool]]:
        where = []
        for key, value in data.items():
            if key in self.model_keys:
                exp = getattr(self.model, key)
                where.append(exp == value)
            else:
                raise ValueError("Key required element in Model")
        return where
