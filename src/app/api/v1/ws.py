from fastapi import APIRouter, WebSocket

router = APIRouter()

@router.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    ...