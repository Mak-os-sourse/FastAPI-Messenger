from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.chat_relationships_crud import chat_relationships_crud
from src.app.deps.auth import auth_user
from src.app.crud.chat import chat_crud
from src.app.models.user import User
from src.app.schemas.chat import (
    ChatResponse, CreateGroupChat
)
from src.app.core.db import db

router = APIRouter(prefix="/chat/group")

@router.post("/create", response_model=ChatResponse)
async def creat_chat(
    user: User = Depends(auth_user),
    create_chat: CreateGroupChat = Body(),
    session: AsyncSession = Depends(db.get_session),
):
    chat = await chat_crud.add(session, **create_chat.model_dump(), type="group")
    await chat_relationships_crud.add(session, chat_id=chat.id, user_id=user.id, is_admin=True)
    return ChatResponse(**chat.model_dump())