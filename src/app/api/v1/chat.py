from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.chat_relationships import ChatRelationships
from src.app.deps.chat import get_chat_admin
from src.app.crud.chat import chat_crud
from src.app.schemas.base import Success
from src.app.schemas.chat import (
    ChatResponse,
    UpdateChat,
)
from src.app.core.db import db

router = APIRouter(prefix="/chat")

@router.put("/update", response_model=ChatResponse)
async def update_chat(
    chat: ChatRelationships = Depends(get_chat_admin),
    update_chat: UpdateChat = Body(),
    session: AsyncSession = Depends(db.get_session),
):
    data = update_chat.model_dump(exclude_none=True)
    return await chat_crud.update(session, id=chat.id, **data)


@router.delete("/delete", response_model=Success)
async def update_chat(
    chat: ChatRelationships = Depends(get_chat_admin),
    session: AsyncSession = Depends(db.get_session),
):
    await chat_crud.delete(session, id=chat.id)
    return Success(success=True)
