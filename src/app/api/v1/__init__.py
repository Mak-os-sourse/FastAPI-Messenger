from fastapi import APIRouter

from src.app.api.v1.auth import router as auth
from src.app.api.v1.user import router as user
from src.app.api.v1.chat import router as chat
from src.app.api.v1.chat_group import router as chat_group
from src.app.api.v1.chat_direct import router as chat_diirect
from src.app.api.v1.invitation import router as invitation

router = APIRouter()
router.include_router(auth)
router.include_router(user)
router.include_router(chat)
router.include_router(chat_group)
router.include_router(chat_diirect)
router.include_router(invitation)