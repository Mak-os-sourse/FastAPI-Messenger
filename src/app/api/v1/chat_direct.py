from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.user import user_crud
from src.app.deps.auth import auth_user
from src.app.crud.chat_direct import chat_direct_crud
from src.app.models.user import User
from src.app.exc.user import UserNotFoud
from src.app.schemas.chat_direct import (
    ChatDirectResponse, CreateDirectChat,
)
from src.app.core.db import db

router = APIRouter(prefix="/chat/direct")

@router.post("/create", response_model=ChatDirectResponse)
async def create_chat(
    user: User = Depends(auth_user),
    create_chat_model: CreateDirectChat = Body(),
    session: AsyncSession = Depends(db.get_session),
):
    companion = await user_crud.get_one(session, id=create_chat_model.companion_id)
    
    if companion is None:
        raise UserNotFoud()

    chat = await chat_direct_crud.add_if_not_exists(session, user_id_one=user.id, user_id_two=create_chat_model.companion_id)
    return ChatDirectResponse(**chat.model_dump())