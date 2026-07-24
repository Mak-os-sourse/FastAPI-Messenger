from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.app.websocket.dispatcher import dp
from src.app.websocket.manager import manager

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