from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.chat_relationships_crud import chat_relationships_crud
from src.app.crud.user import user_crud
from src.app.deps.auth import auth_user
from src.app.crud.chat_direct import chat_direct_crud
from src.app.models.user import User
from src.app.schemas.chat_direct import (
    ChatDirectResponse, CreateDirectChat,
)
from src.app.core.db import db

router = APIRouter(prefix="/chat/direct")

@router.post("/create", response_model=ChatDirectResponse)
async def creat_chat(
    user: User = Depends(auth_user),
    create_chat: CreateDirectChat = Body(),
    session: AsyncSession = Depends(db.get_session),
):
    user = await user_crud.get_one(session, id=create_chat.companion_id)
    
    if user is None:
        raise

    chat = await chat_direct_crud.add(session, **create_chat.model_dump(), type="direct")
    await chat_relationships_crud.add(session, chat_id=chat.id, user_id=user.id, is_admin=True)
    await chat_relationships_crud.add(session, chat_id=chat.id, user_id=create_chat.companion_id, is_admin=True)
    return ChatDirectResponse(**chat.model_dump())