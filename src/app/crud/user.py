from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.models.user import User


class UserCrud(BaseCRUD[User]):
    def __init__(self) -> None:
        super().__init__(User)

    async def add(
        self,
        session: AsyncSession,
        username: str,
        name: str,
        password: str,
        email: str,
        description: str | None = None,
        image: str | None = None,
    ) -> User:
        return await super().add(
            session,
            username=username,
            name=name,
            password=password,
            email=email,
            description=description,
            image=image,
        )


user_crud = UserCrud()
