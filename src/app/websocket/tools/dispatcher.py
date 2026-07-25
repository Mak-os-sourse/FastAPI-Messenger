import json
from fastapi import WebSocket
from typing import AsyncGenerator
from pydantic import BaseModel

from app.websocket.tools.params import params
from app.schemas.websocket import WebSocketResponse
from app.exc.webscoket import WebSocketError, ActionError
from app.websocket.tools.manager import manager
        
class WSRouter:
    def __init__(self):
            self.routers = {}
            
    def router(self, action: str):
        def decorator(func):
            self.routers[action] = func
        return decorator()
    
    def include_routers(self, dp):
        self.routers.update(dp.routers) 

class Dispatcher(WSRouter):
    async def execute_request(self, ws: WebSocket, data: dict) -> None:
        deps = []
        
        try:
            func = self.routers.get(data["action"])
            if func is None:
                raise ActionError()
            
            kwargs, deps = await params.get_kwargs(func=func, data=data)
            result_router = await func(**kwargs)
            if isinstance(result, BaseModel):
                result = result_router.model_dump_json()
            else:
                result = json.dump(result_router)
            
            model = WebSocketResponse(action=data["action"], status="success", data=result)
            await manager.send_personal_message(data=model.model_dump_json(), ws=ws)
        except Exception as e:
            if isinstance(e, WebSocketError):
                name_error = e.name
            else:
                name_error = "ServerError"
            model = WebSocketResponse(action=data["action"], status="error", messege=str(e), error=name_error)
            await manager.send_personal_message(data=model.model_dump_json(), ws=ws)
            raise e

        await self._close_deps(deps)
       
    async def _close_deps(self, deps: list[AsyncGenerator]) -> None:
        for item in deps:
            if isinstance(item, AsyncGenerator):
                await anext(item)
    
dp = Dispatcher()