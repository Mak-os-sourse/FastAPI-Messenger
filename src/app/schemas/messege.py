from pydantic import BaseModel

from app.schemas.websocket import WebSocketRequest

class NewMessegeRequest(WebSocketRequest):
    chat_id: int
    content: str

class NewMessege(BaseModel):
    chat_id: int
    content: str

class DeleteMessege(BaseModel):
    chat_id: int
    messege_id: int

class UpdateMessege(BaseModel):
    chat_id: int
    messege_id: int
    content: str