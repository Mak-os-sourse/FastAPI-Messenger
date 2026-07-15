from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.chat_relationships_crud import chat_relationships_crud
from src.app.models.chat_relationships import ChatRelationships
from src.app.crud.invitation_crud import invitation_crud
from src.app.deps.chat import get_chat_admin
from src.app.deps.auth import auth_user
from src.app.schemas.base import Success
from src.app.models.user import User
from src.app.exc.chat import (
    UserNotAdminInChat,
)
from src.app.schemas.chat import (
    CreateInvitation,
    AcceptInvitation,
    InvitationResponse,
)
from src.app.core.db import db

router = APIRouter(prefix="/chat/invitation")

@router.post("/create", response_model=InvitationResponse)
async def create_invitation(
    chat: ChatRelationships = Depends(get_chat_admin),
    create_invitation: CreateInvitation = Body(),
    session: AsyncSession = Depends(db.get_session),
):
    invitation = await invitation_crud.add(session, **create_invitation.model_dump(), chat_id=chat.id)
    return InvitationResponse(**invitation.model_dump())


@router.delete("/delete", response_model=Success)
async def delete_invitation(
    chat: ChatRelationships = Depends(get_chat_admin),
    session: AsyncSession = Depends(db.get_session),
):
    await invitation_crud.delete(session, id=chat.id)
    return Success(success=True)
    
@router.post("/accept", response_model=Success)
async def accept_invitation(
    user: User = Depends(auth_user),
    accept_invitation: AcceptInvitation = Body(),
    session: AsyncSession = Depends(db.get_session),
):
    invitation = invitation_crud.get_one(session, id=accept_invitation.id, user_id=user.id)
    
    if invitation is not None:
        await chat_relationships_crud.add(
            session,
            chat_id=invitation.chat_id,
            user_id=user.id,
            is_admin=False,
        )
        return Success(success=True)
    else:
        raise UserNotAdminInChat()