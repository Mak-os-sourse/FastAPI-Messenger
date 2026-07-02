from fastapi import APIRouter

from src.app.api.v1.auth import router as auth
from src.app.api.v1.user import router as user

router = APIRouter()
router.include_router(auth)
router.include_router(user)