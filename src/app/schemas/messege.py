from pydantic import BaseModel

from app.websocket.tools.schemas import WebSocketRequest


class Messege(BaseModel):
    chat_id: int
    user_id: int
    content: str
    create_at: int

class MessegeResponse(Messege):
    ...
    
class NewMessegeRequest(WebSocketRequest):
    token: str
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