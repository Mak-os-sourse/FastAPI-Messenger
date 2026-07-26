import inspect
from typing import Coroutine, AsyncGenerator, Any
from pydantic import BaseModel

from app.websocket.tools.deps import WSDependsParams
from app.websocket.tools.manager import manager, ConnectionManager

class RouterParams:
    async def get_kwargs(self, func: Coroutine, data: dict) -> tuple[dict, list]:
        kwargs = {}
        deps = {}
        sig = inspect.signature(func)
        for name, param in sig.parameters.items():
            if isinstance(param.annotation, BaseModel):
                kwargs[name] = param.annotation(**data)
            if isinstance(param.default, WSDependsParams):
                kwargs[name] = await self._get_deps(data=data, deps=deps, model=param.default)
            if param.annotation == ConnectionManager:
                kwargs[name] = manager
        return kwargs, deps
    
    async def _get_deps(self, data: dict, deps: dict, model: WSDependsParams) -> Any:
        func = model.func
        
        if model.use_cache:
            func_result = deps.get(func)
            if func_result is not None:
                return func_result
        
        kwargs_deps, deps_func = await self.get_kwargs(func, data=data)

        if inspect.isasyncgenfunction(func):
            gen = func(**kwargs_deps)
            gen = await anext(gen)
        else:
            gen = await func(**kwargs_deps)  
        
        deps.update(deps_func)
        deps[func] = gen
        return gen
    
params = RouterParams()