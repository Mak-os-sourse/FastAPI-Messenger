from redis.asyncio import Redis
from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.notification import notification
from app.crud.chat_direct import chat_direct_crud
from app.crud.user import user_crud
from app.deps.auth import auth_user
from app.models.user import User
from app.exc.user import UserNotFoud
from app.schemas.chat_direct import (
    ChatDirectResponse, CreateDirectChat,
)
from app.core.cache import cache
from app.core.db import db

router = APIRouter(prefix="/chat/direct")

@router.post("/create", response_model=ChatDirectResponse)
async def create_chat(
    user: User = Depends(auth_user),
    redis: Redis = Depends(cache.get_redis),
    create_chat_model: CreateDirectChat = Body(),
    session: AsyncSession = Depends(db.get_session),
):
    companion = await user_crud.get_one(session, id=create_chat_model.companion_id)
    
    if companion is None:
        raise UserNotFoud()

    chat = await chat_direct_crud.add_if_not_exists(session, user_id_one=user.id, user_id_two=create_chat_model.companion_id)
    notification.add_chat_ids(user_id=user.id, chat_ids=[chat.id])
    notification.add_chat_ids(user_id=create_chat_model.companion_id, chat_ids=[chat.id])
    await notification.add_chat_connections(redis, chat_ids=[chat.id])
    return ChatDirectResponse(**chat.model_dump())