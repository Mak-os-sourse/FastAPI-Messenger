from typing import Any

from app.crud.object import ObjectCrud, ObjectSession
from app.models.user import User


class UserCrud(ObjectCrud[User]):
    def __init__(self) -> None:
        super().__init__(User)

    async def add(
        self,
        session: ObjectSession,
        username: str,
        name: str,
        password: str,
        email: str,
        **kargs: Any,
    ) -> User:
        return await super().add(
            session, username=username, name=name, password=password, email=email, **kargs
        )


user_crud = UserCrud()
