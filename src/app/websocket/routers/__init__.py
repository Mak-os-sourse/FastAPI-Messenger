from app.websocket.routers.messeger import router as messege_router
from app.websocket.tools import WSRouter

router = WSRouter()

router.include_routers(messege_router)