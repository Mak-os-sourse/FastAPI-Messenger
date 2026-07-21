from fastapi import APIRouter, Depends, Body, Query, UploadFile, Response
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path

from src.app.services.avatar_manager import avatar_manager
from src.app.aws import S3Storage, get_storage
from src.app.core.settings import settings
from src.app.deps.file import get_image
from src.app.deps.auth import auth_user
from src.app.crud.user import user_crud
from src.app.schemas.base import Success
from src.app.schemas.user import (
    UserResponse, Enable2FA,
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

@router.delete("/delete", response_model=Success)
async def delete_user(
    user: User = Depends(auth_user),
    session: AsyncSession = Depends(db.get_session)
):
    await user_crud.delete(session, id=user.id)
    return Success(success=True)

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
    user: User = Depends(auth_user),
    image: UploadFile = Depends(get_image),
    storage: S3Storage = Depends(get_storage),
):
    suffix = Path(image.filename).suffix
    await avatar_manager.save(
        storage, id=user.id,
        bucket=settings.s3.user_bucket,
        file=(await image.read()),
        input_format=suffix
    )
    return Success(success=True)

@router.post("/2fa/enable", response_model=Success)
async def enable_2fa(
    enable_2fa: Enable2FA = Body(),
    user: User = Depends(auth_user),
    session: AsyncSession = Depends(db.get_session),
):
    await user_crud.update(session, id=user.id, type_2fa=enable_2fa.type)
    return Success(success=True)

@router.post("/2fa/disable", response_model=Success)
async def enable_2fa(
    user: User = Depends(auth_user),
    session: AsyncSession = Depends(db.get_session),
):
    await user_crud.update(session, id=user.id, type_2fa=None)
    return Success(success=True)