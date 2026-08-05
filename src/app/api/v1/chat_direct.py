from fastapi import APIRouter, Body, Depends, Query
from redis.asyncio import Redis
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import cache
from app.core.db import db
from app.crud.chat_direct import chat_direct_crud
from app.crud.user import user_crud
from app.deps.auth import auth_user
from app.exc.user import UserNotFoud
from app.models.chat_direct import ChatDirect
from app.models.user import User
from app.schemas.base import Success
from app.schemas.chat_direct import (
    ChatDirectResponse,
    CreateDirectChat,
)
from app.services.notification_messeges import notification_messeges

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
    await notification_messeges.subscribe(redis, user_id=user.id, channel_ids=[chat.id])
    return ChatDirectResponse(**chat.model_dump())

@router.delete("/delete", response_model=Success)
async def delete_chat(
    user: User = Depends(auth_user),
    chat_id: int = Query(embed=True),
    session: AsyncSession = Depends(db.get_session),
):
    await chat_direct_crud.delete(session, id=chat_id, whereclause=[or_(
        ChatDirect.user_id_one == user.id,
        ChatDirect.user_id_two == user.id,
    )])
    await notification_messeges.unsubscribe_all(channel_ids=[chat_id])
    return Success(success=True)