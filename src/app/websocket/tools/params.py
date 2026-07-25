import inspect
from typing import Coroutine, AsyncGenerator, Any
from pydantic import BaseModel

from app.websocket.tools.deps import WSDependsParams
from app.websocket.tools.manager import manager, ConnectionManager

class PramasRouter:
    async def get_kwargs(self, func: Coroutine, data: dict) -> tuple[dict, list]:
        kwargs = {}
        deps = []
        sig = inspect.signature(func)
        for name, param in sig.parameters.items():
            if isinstance(param.annotation, BaseModel):
                kwargs[name] = param.annotation(**data)
            if isinstance(param.default, WSDependsParams):
                kwargs[name] = await self._get_deps(deps=deps, func=func)
            if param.annotation == ConnectionManager:
                kwargs[name] = manager
        return kwargs, deps
    
    async def _get_deps(self, deps: list, func: Coroutine | AsyncGenerator) -> Any:
        kwargs_deps, deps_func = self._get_kwargs(func)
        gen = await func(**kwargs_deps)
        
        if isinstance(func, AsyncGenerator):
            gen = await anext(gen)
        
        deps.extend(deps_func)
        deps.append(func)
        return gen
    
params = PramasRouter()