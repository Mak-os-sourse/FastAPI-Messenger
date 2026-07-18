from pydantic import BaseModel, Field

class ChatDirect(BaseModel):
    id: int
    user_id_one: int
    user_id_two: int
    create_at: int

class ChatDirectResponse(ChatDirect):
    ...

class CreateDirectChat(BaseModel):
    companion_id: int