from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.routers import router as dp_router
from app.websocket.tools import dp, manager

dp.include_routers(dp_router)
router = APIRouter()

@router.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            data = await manager.receive_json(ws)
            print(data["action"])
            if data is None:
               await manager.disconnect(ws)
               return
            await dp.execute_request(ws, data=data)
    except WebSocketDisconnect:
        await manager.disconnect(ws)