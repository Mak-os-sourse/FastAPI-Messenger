from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.base import BaseCRUD
from src.app.models.user import User

class UserCrud(BaseCRUD):
    def __init__(self):
        super().__init__(User)
        
    async def add(
        self,
        session: AsyncSession,
        username: str,
        name: str,
        password: str,
        email: str,
        description: str,
        ) -> User:
        return await super().add(
            session,
            username=username,
            name=name,
            password=password,
            email=email,
            description=description,
        )

user_crud = UserCrud()