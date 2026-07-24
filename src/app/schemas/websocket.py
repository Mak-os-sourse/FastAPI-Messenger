from pydantic import BaseModel

class WebSocketRequest(BaseModel):
    action: str

class ChatRequest(WebSocketRequest):
    token: str
    chat_id: int
    
class NewMessege(ChatRequest):
    type: str = "messege"
    content: str

class DeleteMessege(ChatRequest):
    type: str = "messege"
    messege_id: int

class UpdateMessege(ChatRequest):
    type: str = "messege"
    messege_id: int
    content: str