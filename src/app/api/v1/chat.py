from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.chat_relationships_crud import chat_relationships_crud
from src.app.crud.invitation_crud import invitation_crud
from src.app.models.user import User
from src.app.deps.auth import auth_user
from src.app.crud.chat import chat_crud
from src.app.schemas.base import Success
from src.app.schemas.chat import (
    ChatResponse, CreateChat,
    UpdateChat, DeleteChat,
    CreateInvitation,
    InvitationResponse,
)

from src.app.core.db import db

router = APIRouter(prefix="/chat")

@router.post("/create", response_model=ChatResponse)
async def creat_chat(
    user: User = Depends(auth_user),
    create_chat: CreateChat = Body(),
    session: AsyncSession = Depends(db.get_session),
):
    chat = await chat_crud.add(session, **create_chat.model_dump())
    await chat_relationships_crud.add(session, chat_id=chat.id, user_id=user.id, is_admin=True)
    return ChatResponse(**chat.model_dump())

@router.put("/update", response_model=ChatResponse)
async def update_chat(
    user: User = Depends(auth_user),
    update_chat: UpdateChat = Body(),
    session: AsyncSession = Depends(db.get_session),
):
    data = update_chat.model_dump(exclude_none=True)
    chat_id = chat.pop("chat_id")
    
    chat = await chat_relationships_crud.get_one(
        session, chat_id=chat_id,
        user_id=user.id, is_admin=True
    )
    
    if chat is not None:
        return await chat_crud.update(session, id=chat_id, **data)
    else:
        raise

@router.delete("/delete", response_model=Success)
async def update_chat(
    user: User = Depends(auth_user),
    delete_chat: DeleteChat = Body(),
    session: AsyncSession = Depends(db.get_session),
):
    chat = await chat_relationships_crud.get_one(
        session, chat_id=delete_chat.chat_id,
        user_id=user.id, is_admin=True
    )
    
    if chat is not None:
        await chat_crud.delete(session, id=delete_chat.chat_id)
        return Success(success=True)
    else:
        raise

@router.post("/invitation/create", response_model=InvitationResponse)
async def add_user_in_chat(
    user: User = Depends(auth_user),
    create_invitation: CreateInvitation = Body(),
    session: AsyncSession = Depends(db.get_session),
):
    chat = await chat_relationships_crud.get_one(
        session, chat_id=create_invitation.chat_id,
        user_id=user.id, is_admin=True
    )
    
    if chat is not None:
        invitation = await invitation_crud.add(session, **create_invitation.model_dump())
        return InvitationResponse(**invitation.model_dump())
    else:
        raise