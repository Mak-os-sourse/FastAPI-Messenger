from fastapi import APIRouter, Depends, Body, Query, Response, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path

from src.app.crud.chat_relationships_crud import chat_relationships_crud
from src.app.models.chat_relationships import ChatRelationships
from src.app.services.avatar_manager import avatar_manager
from src.app.crud.invitation_crud import invitation_crud
from src.app.crud.chat_group import chat_group_crud
from src.app.aws import S3Storage, get_storage
from src.app.deps.chat import get_chat_admin
from src.app.core.settings import settings
from src.app.deps.file import get_image
from src.app.deps.auth import auth_user
from src.app.schemas.base import Success
from src.app.models.user import User
from src.app.exc.chat import (
    ChatNotFound, InvitationNotFound
)
from src.app.schemas.chat_group import (
    ChatGroupResponse, CreateGroupChat,
    UpdateChat, AcceptJoin
)
from src.app.core.db import db

router = APIRouter(prefix="/chat/group")

@router.post("/create", response_model=ChatGroupResponse)
async def creat_chat(
    user: User = Depends(auth_user),
    create_chat: CreateGroupChat = Body(),
    session: AsyncSession = Depends(db.get_session),
):
    chat = await chat_group_crud.add(session, **create_chat.model_dump())
    await chat_relationships_crud.add(session, chat_id=chat.id, user_id=user.id, is_admin=True)
    return ChatGroupResponse(**chat.model_dump())

@router.put("/update", response_model=ChatGroupResponse)
async def update_chat(
    chat: ChatRelationships = Depends(get_chat_admin),
    update_chat: UpdateChat = Body(),
    session: AsyncSession = Depends(db.get_session),
):
    data = update_chat.model_dump(exclude_none=True)
    return await chat_group_crud.update(session, id=chat.id, **data)

@router.get("/avatar/get")
async def get_avatar(
    id: str = Query(),
    storage: S3Storage = Depends(get_storage),
):
    format = settings.file.base_image_format
    image = await avatar_manager.get(storage, id=id)
    return Response(image, media_type=f"image/{format}")

@router.put("/avatar/update", response_model=Success)
async def update_avatar(
    chat: ChatRelationships = Depends(get_chat_admin),
    image: UploadFile = Depends(get_image),
    storage: S3Storage = Depends(get_storage),
):
    suffix = Path(image.filename).suffix
    await avatar_manager.save(
        storage, id=chat.chat_id,
        bucket=settings.s3.chat_bucket,
        file=(await image.read()),
        input_format=suffix
    )
    return Success(success=True)

@router.delete("/delete", response_model=Success)
async def delete_chat(
    chat: ChatRelationships = Depends(get_chat_admin),
    session: AsyncSession = Depends(db.get_session),
):
    await chat_group_crud.delete(session, id=chat.id)
    return Success(success=True)

@router.post("/join", response_model=Success)
async def join_user(
    user: User = Depends(auth_user),
    chat_id: int = Body(embed=True),
    session: AsyncSession = Depends(db.get_session)
):
    chat_relationships = await chat_relationships_crud.get_one(session, chat_id=chat_id, user_id=user.id)
    chat = await chat_group_crud.get_one(session, id=chat_id)
    
    if chat_relationships is not None or chat is None:
        raise ChatNotFound()
    elif chat.type == "private":
        await invitation_crud.add(session, chat_id=chat_id, user_id=user.id)
    else:
        await chat_relationships_crud.add(session, chat_id=chat_id, user_id=user.id, is_admin=False)
        
    return Success(success=True)
        
@router.post("/accept-join", response_model=Success)
async def accept_join(
    chat: ChatRelationships = Depends(get_chat_admin),
    accept_join: AcceptJoin = Body(),
    session: AsyncSession = Depends(db.get_session),
):
    invitation = await invitation_crud.get_one(session, id=accept_join.invitation_id)
    
    if invitation is None:
        raise InvitationNotFound()
    
    await chat_relationships_crud.add(session, chat_id=chat.chat_id, user_id=invitation.user_id, is_admin=accept_join.is_admin)
    return Success(success=True)

@router.post("/extended-rights", response_model=Success)
async def extended_rights(
    chat: ChatRelationships = Depends(get_chat_admin),
    user_id: int = Body(embed=True),
    session: AsyncSession = Depends(db.get_session),
):
    await chat_relationships_crud.extended_rights(session, user_id=user_id, chat_id=chat.chat_id)
    return Success(success=True)