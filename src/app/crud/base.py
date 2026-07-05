from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update, delete, BinaryExpression

from src.app.core.base import TModel

class BaseCRUD:
    def __init__(self, model: TModel):
        self.model = model
        self.model_keys = model.__dict__
    
    async def add(self, session: AsyncSession, **values) -> TModel:
        stmt = insert(self.model).values(**values).returning(self.model)
        result = await session.scalars(stmt)
        await session.flush()
        return result.one()
    
    async def get_all(self, session: AsyncSession, whereclause: list[BinaryExpression] = None, **equality_where) -> list[TModel]:
        data = self.get_where(**equality_where)
        stmt = select(self.model).where(*data, *whereclause if whereclause is not None else [])
        result = await session.scalars(stmt)
        return result.all()
    
    async def get_one(self, session: AsyncSession, whereclause: list[BinaryExpression] = None, **equality_where) -> TModel | None:
        result = await self.get_all(session, **equality_where, whereclause=whereclause)
        if result:
            return result[0]
    
    async def update(self, session: AsyncSession, id: int, **values) -> TModel:
        stmt = update(self.model).where(self.model.id == id).values(**values).returning(self.model)
        resutl = await session.scalars(stmt)
        await session.flush()
        return resutl.one()
    
    async def delete(self, session: AsyncSession, id: int, whereclause: list[BinaryExpression] = None, **equality_where) -> None:
        data = self.get_where(**equality_where)
        stmt = delete(self.model).where(*data, self.model.id == id, *whereclause if whereclause is not None else [])
        await session.execute(stmt)
        await session.flush()
    
    def get_where(self, **data) -> list[BinaryExpression]:
        where = []
        for key, value in data.items():
            if key in self.model_keys:
                exp = getattr(self.model, key)
                where.append(exp == value)
        return where
                