from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.deps.auth import auth_user
from src.app.crud.user import user_crud
from src.app.schemas.user import UserResponse
from src.app.models.user import User
from src.app.core.db import db

router = APIRouter(prefix="/user")

@router.get("/me", response_model=UserResponse)
async def get_me(user: User = Depends(auth_user)):
    return UserResponse(**user.model_dump())

