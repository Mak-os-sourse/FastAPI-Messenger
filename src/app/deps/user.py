from fastapi import Depends, Query

from app.crud.object import ObjectSession
from app.crud.user import user_crud
from app.exc.user import UserNotFoud
from app.models.user import User


async def get_user(user_id: int = Query(), session: ObjectSession = Depends()) -> User:
    user = await user_crud.get_one(session, id=user_id)
    if user is not None:
        return user
    raise UserNotFoud()
