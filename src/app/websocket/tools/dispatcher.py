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
    request_model: type[WebSocketRequest] | None


class BaseRouter:
    def __init__(self) -> None:
        self.routers: dict[str, FuncData] = {}


class WSRouter(BaseRouter):
    def __init__(self) -> None:
        super().__init__()

    def router(
        self,
        action: str,
        request_model: type[WebSocketRequest] | None = None,
    ) -> Callable[..., Any]:
        def decorator(func: Callable[..., Any]) -> None:
            if request_model is not None and not issubclass(request_model, WebSocketRequest):
                raise ValueError("request_model must be a subclass of WebSocketRequest")
            self.routers[action] = FuncData(func=func, request_model=request_model)

        return decorator

    def include_routers(self, router: BaseRouter) -> None:
        self.routers.update(router.routers)


class Dispatcher(WSRouter):
    def __init__(self) -> None:
        super().__init__()
        self.dependency_overrides: dict[Any, Any] = {}

    async def execute_request(self, ws: WebSocket, data: dict[Any, Any]) -> None:
        deps: dict[Callable[..., Any], Any] = {}

        try:
            model: FuncData | None = self.routers.get(data["action"])
            if model is None:
                raise ActionError()

            if model.request_model is not None:
                model.request_model(**data)
            func = model.func

            kwargs, deps = await params.get_signature_data(
                func=func,
                data=data,
                dependency_overrides=self.dependency_overrides,
            )
            result_router = await func(**kwargs)
            if isinstance(result_router, BaseModel):
                result_router = result_router.model_dump()

            result_model = WebSocketResponse(
                action=data["action"],
                status="success",
                data=result_router,
            )
            await manager.send_personal_message(data=result_model.model_dump_json(), websocket=ws)
        except Exception as e:
            name_error = self._get_name_error(e)
            result_model = WebSocketResponse(
                action=data["action"],
                status="error",
                messege=str(e),
                error=name_error,
            )
            await manager.send_personal_message(data=result_model.model_dump_json(), websocket=ws)
            raise e

        await params.close_deps(deps)

    def _get_name_error(self, e: Exception) -> str:
        if isinstance(e, WebSocketError):
            return e.name
        if isinstance(e, ValidationError):
            return "ValidationError"
        return "ServerError"
