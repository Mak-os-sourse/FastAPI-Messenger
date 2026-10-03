from fastapi import APIRouter, Body, Depends, Query

from app.crud.chat_direct import chat_direct_crud
from app.crud.object import ObjectSession
from app.crud.user import user_crud
from app.deps.auth import auth_user
from app.exc.chat import ChatAlredyCreated
from app.exc.user import UserNotFoud
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
    object_session: ObjectSession = Depends(),
) -> ChatDirectResponse:
    companion = await user_crud.get_one(object_session, id=create_chat_model.companion_id)

    if companion is None:
        raise UserNotFoud()

    chat = await chat_direct_crud.add_if_not_exists(
        object_session,
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
    object_session: ObjectSession = Depends(),
) -> Success:
    await chat_direct_crud.delete_by_user_id(object_session, id=chat_id, user_id=user.id)
    return Success(success=True)
