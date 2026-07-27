import inspect
from typing import Coroutine, AsyncGenerator, Any
from pydantic import BaseModel

from app.websocket.tools.deps import WSDependsParams
from app.websocket.tools.manager import manager, ConnectionManager

class RouterParams:
    async def get_kwargs(self, func: Coroutine, data: dict, dependency_overrides: dict) -> tuple[dict, list]:
        kwargs = {}
        deps = {}
        sig = inspect.signature(func)
        for name, param in sig.parameters.items():
            if issubclass(param.annotation, BaseModel):
                kwargs[name] = param.annotation(**data)
            if isinstance(param.default, WSDependsParams):
                kwargs[name] = await self._get_deps(model=param.default, deps=deps, dependency_overrides=dependency_overrides, data=data)
            if param.annotation == ConnectionManager:
                kwargs[name] = manager
        return kwargs, deps
    
    async def _get_deps(self, model: WSDependsParams, deps: dict, dependency_overrides: dict, data: dict) -> Any:
        func = dependency_overrides[model.func] if dependency_overrides.get(model.func, False) else model.func
        
        if model.use_cache:
            func_result = deps.get(func)
            if func_result is not None:
                return func_result
        
        kwargs_deps, deps_func = await self.get_kwargs(func, data=data, dependency_overrides=dependency_overrides)

        if inspect.isasyncgenfunction(func):
            gen = func(**kwargs_deps)
            gen = await anext(gen)
        if inspect.iscoroutinefunction(func):
            gen = await func(**kwargs_deps)   
        else:
            gen = func(**kwargs_deps)
        
        deps.update(deps_func)
        deps[func] = gen
        return gen
    
    async def close_deps(self, deps: dict) -> None:
        for item in deps.keys():
            if inspect.isasyncgenfunction(item):
                await anext(item)
    
params = RouterParams()