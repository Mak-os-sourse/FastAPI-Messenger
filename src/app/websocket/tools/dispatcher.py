from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from fastapi import WebSocket
from pydantic import BaseModel, ValidationError

from app.websocket.tools.exc import ActionError, WebSocketError
from app.websocket.tools.manager import manager
from app.websocket.tools.params import params
from app.websocket.tools.schemas import WebSocketRequest, WebSocketResponse


@dataclass
class FuncData:
    func: Callable[..., Any]
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
        deps: dict[Callable[..., Any], Any] = {}
        
        try:
            model: FuncData | None = self.routers.get(data["action"])
            if model is None:
                raise ActionError()
            else:
                model.request_model(**data)
                func = model.func
            
            kwargs, deps = await params.get_signature_data(func=func, data=data, dependency_overrides=self.dependency_overrides)
            result_router = await func(**kwargs)
            if isinstance(result_router, BaseModel):
                result_router = result_router.model_dump()
            
            result_model = WebSocketResponse(action=data["action"], status="success", data=result_router)
            await manager.send_personal_message(data=result_model.model_dump_json(), websocket=ws)
        except Exception as e:
            name_error = self._get_name_error(e)
            result_model = WebSocketResponse(action=data["action"], status="error", messege=str(e), error=name_error)
            await manager.send_personal_message(data=result_model.model_dump_json(), websocket=ws)
            raise e

        await params.close_deps(deps)
        
    def _get_name_error(self, e: Exception):
        if isinstance(e, WebSocketError):
            return e.name
        elif isinstance(e, ValidationError):
            return "ValidationError"
        else:
            return"ServerError"