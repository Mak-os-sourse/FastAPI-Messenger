from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.chat_relationships_crud import chat_relationships_crud
from src.app.models.chat_relationships import ChatRelationships
from src.app.exc.chat import UserNotAdminInChat
from src.app.deps.auth import auth_user
from src.app.models.user import User
from src.app.core.db import db

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