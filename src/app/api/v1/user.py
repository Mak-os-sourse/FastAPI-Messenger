from fastapi import APIRouter, Depends, Body, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.deps.file import get_image
from src.app.deps.auth import auth_user
from src.app.crud.user import user_crud
from src.app.schemas.user import (
    UserResponse, Enable2FA,
    Enable2FAResponse,
    UpdateData,
)
from src.app.models.user import User
from src.app.core.db import db

router = APIRouter(prefix="/user")

@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(auth_user)):
    return UserResponse(**user.model_dump())

@router.put("/data/update", response_model=UserResponse)
async def update_data(
    user: User = Depends(auth_user),
    update_data: UpdateData = Body(),
    session: AsyncSession = Depends(db.get_session)
):
    data = update_data.model_dump(exclude_none=True)
    user = await user_crud.update(session, id=user.id, **data)
    return UserResponse(**user.model_dump())
    
@router.put("/avatar/update")
async def update_avatar(
    user: User = Depends(auth_user),
    image: UploadFile = Depends(get_image),
):
    ...

@router.post("/2fa/enable", response_model=Enable2FAResponse)
async def enable_2fa(
    enable_2fa: Enable2FA = Body(),
    user: User = Depends(auth_user),
    session: AsyncSession = Depends(db.get_session),
):
    await user_crud.update(session, id=user.id, type_2fa=enable_2fa.type)
    return Enable2FAResponse(enable_2fa=True, type=enable_2fa.type)

@router.post("/2fa/disable", response_model=Enable2FAResponse)
async def enable_2fa(
    user: User = Depends(auth_user),
    session: AsyncSession = Depends(db.get_session),
):
    await user_crud.update(session, id=user.id, type_2fa=None)
    return Enable2FAResponse(enable_2fa=False, type=None)