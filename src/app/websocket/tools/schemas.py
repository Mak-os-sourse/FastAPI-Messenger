from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class WebSocketNotificationResponse(BaseModel):
    action: str
    messege: str | None = None
    data: dict[Any, Any] = {}


class WebSocketRequest(BaseModel):
    action: str

    model_config = ConfigDict(extra="forbid")


class WebSocketResponse(BaseModel):
    action: str
    messege: str | None = None
    status: Literal["success", "error", "process"]
    data: dict[Any, Any] = {}
    error: str | None = None
