from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import db
from app.crud.chat_relationships import chat_relationships_crud
from app.deps.auth import auth_user
from app.exc.chat import UserNotAdminInChat
from app.models.chat_relationships import ChatRelationships
from app.models.user import User


async def get_chat_admin(
    chat_id: int = Query(),
    user: User = Depends(auth_user),
    session: AsyncSession = Depends(db.get_session),
) -> ChatRelationships | None:
    chat = await chat_relationships_crud.get_one(
        session, chat_id=chat_id,
        user_id=user.id, is_admin=True
    )
    
    if chat is None:
        raise UserNotAdminInChat()
    
    return chat