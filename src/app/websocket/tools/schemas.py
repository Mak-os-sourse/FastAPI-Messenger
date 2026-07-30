from typing import Literal

from pydantic import BaseModel, ConfigDict


class WebSocketNotificationResponse(BaseModel):
    action: str
    type: str
    messege: str | None = None
    data: dict = {}

class WebSocketRequest(BaseModel):
    action: str
    
    model_config = ConfigDict(extra='forbid')

class WebSocketResponse(BaseModel):
    action: str
    messege: str | None = None
    status: Literal["success", "error", "process"]
    data: dict = {}
    error: str | None = None