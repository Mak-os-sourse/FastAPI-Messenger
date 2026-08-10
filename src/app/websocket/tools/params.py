import inspect
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel

from app.websocket.tools.deps import WSDependsParams
from app.websocket.tools.manager import ConnectionManager, manager


class RouterParams:
    async def get_signature_data(
        self,
        func: Callable[..., Any],
        data: dict[Any, Any],
        dependency_overrides: dict[Callable[..., Any], Any],
    ) -> tuple[dict[Any, Any], dict[Any, Any]]:
        """Use kwargs, deps = parse_signature(...)"""
        kwargs: dict[str, Any] = {}
        deps: dict[Callable[..., Any], Any] = {}
        sig = inspect.signature(func)
        for name, param in sig.parameters.items():
            if issubclass(param.annotation, BaseModel):
                kwargs[name] = param.annotation(**data)
            if isinstance(param.default, WSDependsParams):
                kwargs[name] = await self._get_dependence(
                    model=param.default,
                    deps=deps,
                    dependency_overrides=dependency_overrides,
                    data=data,
                )
            if param.annotation == ConnectionManager:
                kwargs[name] = manager
        return kwargs, deps

    async def close_deps(self, deps: dict[Callable[..., Any], Any]) -> None:
        for item in deps:
            if inspect.isasyncgen(item):
                await anext(item)
                await item.aclose()
            elif inspect.isgenerator(item):
                next(item)
                item.close()

    async def _get_dependence(
        self,
        model: WSDependsParams,
        deps: dict[Callable[..., Any], Any],
        dependency_overrides: dict[Callable[..., Any], Any],
        data: dict[Any, Any],
    ) -> Any:
        if dependency_overrides.get(model.func, False):
            func = dependency_overrides[model.func]
        else:
            func = model.func

        if model.use_cache:
            func_result = deps.get(func)
            if func_result is not None:
                return func_result

        kwargs_deps, deps_func = await self.get_signature_data(
            func,
            data=data,
            dependency_overrides=dependency_overrides,
        )

        gen, result = await self._get_func_data(func, **kwargs_deps)

        deps.update(deps_func)
        deps[func] = gen
        return result

    async def _get_func_data(self, func: Any, **kwargs_deps: Any) -> tuple[Any, Any]:
        if inspect.isasyncgenfunction(func):
            gen = func(**kwargs_deps)
            return gen, await anext(gen)
        if inspect.isgeneratorfunction(func):
            gen = func(**kwargs_deps)
            return gen, next(gen)
        if inspect.iscoroutinefunction(func):
            gen = await func(**kwargs_deps)
            return func, gen
        gen = func(**kwargs_deps)
        return func, gen


params = RouterParams()
