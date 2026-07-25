from app.websocket.tools import WSRouter

from app.websocket.routers.messeger import router as messege_router

router = WSRouter()

router.include_routers(messege_router)