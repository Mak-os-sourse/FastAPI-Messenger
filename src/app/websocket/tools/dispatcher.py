import json
from fastapi import WebSocket
from pydantic import BaseModel, ValidationError
from dataclasses import dataclass
from typing import Coroutine

from app.websocket.tools.params import params
from app.websocket.tools.schemas import WebSocketResponse, WebSocketRequest
from app.websocket.tools.exc import WebSocketError, ActionError
from app.websocket.tools.manager import manager

@dataclass
class FuncData:
    func: Coroutine
    request_model: type[BaseModel] | None

class WSRouter:
    def __init__(self):
        self.routers: dict[str, FuncData] = {}
            
    def router(self, action: str, request_model: type[BaseModel] | None = None):
        def decorator(func):
            if not issubclass(request_model, WebSocketRequest):
                raise ValueError("request_model must be a subclass of WebSocketRequest")
            self.routers[action] = FuncData(func=func, request_model=request_model)
        return decorator
    
    def include_routers(self, dp):
        self.routers.update(dp.routers)

class Dispatcher(WSRouter):
    def __init__(self):
        super().__init__()
        self.dependency_overrides = {}
   
    async def execute_request(self, ws: WebSocket, data: dict) -> None:
        deps = []
        
        try:
            model = self.routers.get(data["action"])
            model.request_model(**data)
            func = model.func
            if func is None:
                raise ActionError()
            
            kwargs, deps = await params.get_kwargs(func=func, data=data, dependency_overrides=self.dependency_overrides)
            result_router = await func(**kwargs)
            if isinstance(result_router, BaseModel):
                result_router = result_router.model_dump_json()
            
            model = WebSocketResponse(action=data["action"], status="success", data=result_router)
            await manager.send_personal_message(data=model.model_dump_json(), websocket=ws)
        except Exception as e:
            if isinstance(e, WebSocketError):
                name_error = e.name
            elif isinstance(e, ValidationError):
                name_error = "ValidationError"
            else:
                name_error = "ServerError"
            model = WebSocketResponse(action=data["action"], status="error", messege=str(e), error=name_error)
            await manager.send_personal_message(data=model.model_dump_json(), websocket=ws)
            print(e)
            # raise e

        await params.close_deps(deps)