from pathlib import Path

from fastapi import APIRouter, Body, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import db
from app.core.settings import settings
from app.crud.chat_group import chat_group_crud
from app.crud.chat_relationships import chat_relationships_crud
from app.crud.invitation import invitation_crud
from app.deps.auth import auth_user
from app.deps.chat import get_chat_admin
from app.deps.file import get_image
from app.exc.chat import ChatNotFound, InvitationNotFound
from app.models.chat_relationships import ChatRelationships
from app.models.user import User
from app.schemas.base import Success
from app.schemas.chat_group import (
    AcceptJoin,
    ChatGroupResponse,
    CreateGroupChat,
    UpdateChat,
)
from app.services.avatar_manager import avatar_manager

router = APIRouter(prefix="/chat/group", tags=["Chat-group"])


@router.post("/create", response_model=ChatGroupResponse)
async def creat_chat(
    user: User = Depends(auth_user),
    create_chat: CreateGroupChat = Body(),
    session: AsyncSession = Depends(db.get_session),
) -> ChatGroupResponse:
    chat = await chat_group_crud.add(session, **create_chat.model_dump())
    await chat_relationships_crud.add(session, chat_id=chat.id, user_id=user.id, is_admin=True)
    return ChatGroupResponse(**chat.model_dump())


@router.put("/update", response_model=ChatGroupResponse)
async def update_chat(
    relation: ChatRelationships = Depends(get_chat_admin),
    update_chat: UpdateChat = Body(),
    session: AsyncSession = Depends(db.get_session),
) -> ChatGroupResponse:
    data = update_chat.model_dump(exclude_none=True)
    result = await chat_group_crud.update(session, id=relation.id, **data)
    return ChatGroupResponse(**result.model_dump())


@router.delete("/delete", response_model=Success)
async def delete_chat(
    relation: ChatRelationships = Depends(get_chat_admin),
    session: AsyncSession = Depends(db.get_session),
) -> Success:
    await chat_group_crud.delete(session, id=relation.id)
    return Success(success=True)


@router.put("/avatar/update", response_model=Success)
async def update_avatar(
    relation: ChatRelationships = Depends(get_chat_admin),
    image: UploadFile = Depends(get_image),
    session: AsyncSession = Depends(db.get_session),
) -> Success:
    suffix = Path(image.filename or "base.png").suffix
    await avatar_manager.save(
        id=relation.chat_id,
        bucket=settings.s3.chat_bucket,
        file=(await image.read()),
        input_format=suffix,
    )
    await chat_group_crud.update(
        session,
        relation.id,
        image=avatar_manager.get_url_file(id=relation.id, bucket=settings.s3.chat_bucket),
    )
    return Success(success=True)


@router.post("/join", response_model=Success)
async def join_user(
    user: User = Depends(auth_user),
    chat_id: int = Body(embed=True),
    session: AsyncSession = Depends(db.get_session),
) -> Success:
    chat_relationships = await chat_relationships_crud.get_one(
        session,
        chat_id=chat_id,
        user_id=user.id,
    )
    chat = await chat_group_crud.get_one(session, id=chat_id)

    if chat_relationships is not None or chat is None:
        raise ChatNotFound()
    if chat.type == "private":
        await invitation_crud.add(session, chat_id=chat_id, user_id=user.id)
    else:
        await chat_relationships_crud.add(session, chat_id=chat_id, user_id=user.id, is_admin=False)

    return Success(success=True)


@router.post("/accept-join", response_model=Success)
async def accept_join(
    chat: ChatRelationships = Depends(get_chat_admin),
    accept_join: AcceptJoin = Body(),
    session: AsyncSession = Depends(db.get_session),
) -> Success:
    invitation = await invitation_crud.get_one(session, id=accept_join.invitation_id)

    if invitation is None:
        raise InvitationNotFound()

    await chat_relationships_crud.add(
        session,
        chat_id=chat.chat_id,
        user_id=invitation.user_id,
        is_admin=accept_join.is_admin,
    )
    return Success(success=True)


@router.post("/extended-rights", response_model=Success)
async def extended_rights(
    chat: ChatRelationships = Depends(get_chat_admin),
    user_id: int = Body(embed=True),
    session: AsyncSession = Depends(db.get_session),
) -> Success:
    await chat_relationships_crud.extended_rights(session, user_id=user_id, chat_id=chat.chat_id)
    return Success(success=True)


@router.post("/leave", response_model=Success)
async def leave(
    user: User = Depends(auth_user),
    chat_id: int = Body(embed=True),
    session: AsyncSession = Depends(db.get_session),
) -> Success:
    await chat_relationships_crud.leave(session, chat_id=chat_id, user_id=user.id)
    return Success(success=True)
