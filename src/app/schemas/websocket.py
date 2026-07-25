from typing import Literal
from pydantic import BaseModel

class WebSocketRequest(BaseModel):
    action: str

class WebSocketResponse(BaseModel):
    action: str
    messege: str | None = None
    status: Literal["success", "error", "process"]
    data: dict = {}
    error: str | None = None

class NewMessege(BaseModel):
    chat_id: int
    type: str = "messege"
    content: str

class DeleteMessege(BaseModel):
    chat_id: int
    type: str = "messege"
    messege_id: int

class UpdateMessege(BaseModel):
    chat_id: int
    type: str = "messege"
    messege_id: int
    content: str