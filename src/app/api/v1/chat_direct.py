from fastapi import APIRouter, Body, Depends, Query
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import db
from app.crud.chat_direct import chat_direct_crud
from app.crud.user import user_crud
from app.deps.auth import auth_user
from app.exc.chat import ChatAlredyCreated
from app.exc.user import UserNotFoud
from app.models.chat_direct import ChatDirect
from app.models.user import User
from app.schemas.base import Success
from app.schemas.chat_direct import (
    ChatDirectResponse,
    CreateDirectChat,
)

router = APIRouter(prefix="/chat/direct", tags=["Chat-direct"])


@router.post("/create", response_model=ChatDirectResponse)
async def create_chat(
    user: User = Depends(auth_user),
    create_chat_model: CreateDirectChat = Body(),
    session: AsyncSession = Depends(db.get_session),
) -> ChatDirectResponse:
    companion = await user_crud.get_one(session, id=create_chat_model.companion_id)

    if companion is None:
        raise UserNotFoud()

    chat = await chat_direct_crud.add_if_not_exists(
        session,
        user_id_one=user.id,
        user_id_two=create_chat_model.companion_id,
    )
    if chat is None:
        raise ChatAlredyCreated()
    return ChatDirectResponse(**chat.model_dump())


@router.delete("/delete", response_model=Success)
async def delete_chat(
    user: User = Depends(auth_user),
    chat_id: int = Query(embed=True),
    session: AsyncSession = Depends(db.get_session),
) -> Success:
    await chat_direct_crud.delete(
        session,
        id=chat_id,
        whereclause=[
            or_(
                ChatDirect.user_id_one == user.id,
                ChatDirect.user_id_two == user.id,
            ),
        ],
    )
    return Success(success=True)
