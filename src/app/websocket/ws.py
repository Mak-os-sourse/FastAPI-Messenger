from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.routers import router
from app.websocket.tools import dp, manager

dp.include_routers(router)
router = APIRouter()

@router.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            data = await manager.receive_json()
            dp.execute_request(data)
    except WebSocketDisconnect:
        manager.disconnect(ws)