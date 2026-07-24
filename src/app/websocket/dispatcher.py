import inspect
from dataclasses import dataclass
from typing import Coroutine, AsyncGenerator
from pydantic import ValidationError

from src.app.websocket.manager import manager
from src.app.schemas.websocket import WebSocketRequest
from src.app.websocket.manager import ConnectionManager

@dataclass
class WSDependsParams:
    func: AsyncGenerator | Coroutine

def WSDpends(func: AsyncGenerator | Coroutine):
    return WSDependsParams(func)

class Dispatcher:
    def __init__(self):
        self.routers = {}
        
    def router(self, active: str):
        def decorator(func):
            self.routers[active] = func
        return decorator()
    
    async def execute_request(self, data: dict) -> None:
        func = self.routers.get(data["active"])
        if func is None:
            raise
        
        kwargs, deps = self._get_kwargs(func=func, data=data)
        
        await func(**kwargs)

        await self._close_deps(deps)
        
    async def _get_kwargs(self, func: Coroutine, data: dict) -> tuple[dict, list]:
        kwargs = {}
        deps = []
        sig = inspect.signature(func)
        for name, param in sig.parameters.items():
            if isinstance(param.annotation, WebSocketRequest):
                kwargs[name] = self.data_to_model(model=param.annotation, data=data)
            if isinstance(param.default, WSDependsParams):
                gen = self._get_deps(param.default)
                deps.append(gen)
                kwargs[name] = gen
            if param.annotation == ConnectionManager:
                kwargs[name] = manager
        return kwargs, deps
    
    def _data_to_model(self, model: WebSocketRequest, data: dict) -> WebSocketRequest:
        try:
            return model(**data)
        except ValidationError:
            raise
    
    async def _get_deps(self, data: WSDependsParams):
        gen = await data.func()
        if isinstance(data, AsyncGenerator):
            anext(gen)
        return gen
            
    async def _close_deps(self, deps: list[AsyncGenerator]) -> None:
        for item in deps:
            if isinstance(item, AsyncGenerator):
                await anext(item)
    
dp = Dispatcher()