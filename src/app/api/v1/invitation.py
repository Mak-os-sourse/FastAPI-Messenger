from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.chat_relationships_crud import chat_relationships_crud
from src.app.crud.invitation_crud import invitation_crud
from src.app.deps.auth import auth_user
from src.app.schemas.base import Success
from src.app.models.user import User
from src.app.schemas.chat import (
    CreateInvitation,
    DeleteInvitation,
    InvitationResponse,
)
from src.app.core.db import db

router = APIRouter(prefix="/chat/invitation")

@router.post("/create", response_model=InvitationResponse)
async def create_invitation(
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

@router.delete("/delete", response_model=Success)
async def delete_invitation(
    user: User = Depends(auth_user),
    delete_invitation: DeleteInvitation = Body(),
    session: AsyncSession = Depends(db.get_session),
):
    chat = await chat_relationships_crud.get_one(
        session, chat_id=create_invitation.chat_id,
        user_id=user.id, is_admin=True
    )
    
    if chat is not None:
        await invitation_crud.delete(session, id=delete_invitation.id)
        return Success(success=True)
    else:
        raise