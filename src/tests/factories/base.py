from typing import Coroutine
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.base import TModel

class BaseFactory:
    def __init__(self, model: TModel):
        self.model = model
    
    def get_data(self) -> dict: ...
    
    async def add(self, session: AsyncSession, count: int = 1, **kargs):
        models = []
        for _ in range(count):
            dict_data = self.get_data()
            dict_data.update(**kargs)
            for key, value in dict_data.items():
                if isinstance(value, Coroutine):
                    dict_data[key] = await value
            
            models.append(self.model(**dict_data))
        session.add_all(models)
        await session.flush()
        return models[0] if len(models) == 1 else models
