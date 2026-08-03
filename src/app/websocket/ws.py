import asyncio

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.cache import cache
from app.core.db import db
from app.crud.chat_relationships import chat_relationships_crud
from app.services.notification_messeges import notification_messeges
from app.websocket.routers import router as dp_router
from app.websocket.tools import Dispatcher, WebSocketNotificationResponse, manager

dp = Dispatcher()
dp.include_routers(dp_router)
router = APIRouter()

@router.websocket("/ws/{user_id}")
async def ws_endpoint(
    ws: WebSocket,
    user_id: int,
    redis: Redis = Depends(cache.get_redis),
    session: AsyncSession = Depends(db.get_session)):
    async def reader(ws: WebSocket):
        while True:
            data = await manager.receive_json(ws)
            if data is None:
                await manager.disconnect(ws)
                return
            await dp.execute_request(ws, data=data)
    
    async def wait_notification(ws: WebSocket, user_id: int):
        data = await chat_relationships_crud.get_all(session, user_id=user_id)
        channel_ids = [item.chat_id for item in data]
        await notification_messeges.subscribe(redis, user_id=user_id, channel_ids=channel_ids)
        
        async for messege in notification_messeges.listen(user_id):
            await ws.send_text(WebSocketNotificationResponse(**messege).model_dump_json())

    await manager.connect(ws)
    try:
        async with asyncio.TaskGroup() as group:
            group.create_task(reader(ws))
            group.create_task(wait_notification(ws, user_id))
    except WebSocketDisconnect:
        await manager.disconnect(ws)