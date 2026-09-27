from pathlib import Path

from fastapi import APIRouter, Body, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import db
from app.core.settings import settings
from app.crud.user import user_crud
from app.deps.auth import auth_user
from app.deps.file import get_image
from app.models.user import User
from app.schemas.base import Success
from app.schemas.user import (
    Enable2FA,
    UpdateData,
    UserResponse,
)
from app.services.avatar_manager import avatar_manager

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(auth_user)) -> UserResponse:
    return UserResponse(**user.model_dump())


@router.put("/data/update", response_model=UserResponse)
async def update_data(
    user: User = Depends(auth_user),
    update_data: UpdateData = Body(),
    session: AsyncSession = Depends(db.get_session),
) -> UserResponse:
    data = update_data.model_dump(exclude_none=True)
    user = await user_crud.update(session, id=user.id, **data)
    return UserResponse(**user.model_dump())


@router.delete("/delete", response_model=Success)
async def delete_user(
    user: User = Depends(auth_user),
    session: AsyncSession = Depends(db.get_session),
) -> Success:
    await user_crud.delete(session, id=user.id)
    return Success(success=True)


@router.put("/avatar/update", response_model=Success)
async def update_avatar(
    user: User = Depends(auth_user),
    image: UploadFile = Depends(get_image),
    session: AsyncSession = Depends(db.get_session),
) -> Success:
    suffix = Path(image.filename or "base.png").suffix
    await avatar_manager.save(
        id=user.id,
        bucket=settings.s3.user_bucket,
        file=(await image.read()),
        input_format=suffix,
    )
    await user_crud.update(
        session,
        user.id,
        image=avatar_manager.get_url_file(id=user.id, bucket=settings.s3.user_bucket),
    )
    return Success(success=True)


@router.post("/2fa/enable", response_model=Success)
async def enable_2fa(
    enable_2fa: Enable2FA = Body(),
    user: User = Depends(auth_user),
    session: AsyncSession = Depends(db.get_session),
) -> Success:
    await user_crud.update(session, id=user.id, type_2fa=enable_2fa.type)
    return Success(success=True)


@router.post("/2fa/disable", response_model=Success)
async def disable_2fa(
    user: User = Depends(auth_user),
    session: AsyncSession = Depends(db.get_session),
) -> Success:
    await user_crud.update(session, id=user.id, type_2fa=None)
    return Success(success=True)
