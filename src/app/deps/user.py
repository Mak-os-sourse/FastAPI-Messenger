from fastapi import Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.exc.user import UserNotFoud
from src.app.crud.user import user_crud
from src.app.models.user import User
from src.app.core.db import db

async def get_user(user_id: int = Body(embed=True), session: AsyncSession = Depends(db.get_session)) -> User:
    user = await user_crud.get_one(session, id=user_id)
    if user is not None:
        return user
    else:
        raise UserNotFoud()