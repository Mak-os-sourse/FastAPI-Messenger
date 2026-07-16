from pydantic import BaseModel, Field

class ChatDirect(BaseModel):
    id: str
    user_id_one: int
    user_id_two: int
    create_at: int

class ChatDirectResponse(ChatDirect):
    ...

class CreateDirectChat(BaseModel):
    companion_id: int
    name: str | None = Field(default=None, max_length=30)
    description: str = Field(default=None, max_length=50)
