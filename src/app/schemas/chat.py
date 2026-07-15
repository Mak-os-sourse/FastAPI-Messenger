from typing import Literal
from pydantic import BaseModel, Field

class Chat(BaseModel):
    id: int
    type: Literal["direct", "group"]
    name: str = Field(max_length=30)
    description: str | None = Field(max_length=50)
    create_at: int

class Invitation(BaseModel):
    id: int
    chat_id: int
    user_id: int

class ChatResponse(Chat):
    ...

class InvitationResponse(Invitation):
    ...

class CreateGroupChat(BaseModel):
    name: str = Field(max_length=30)
    description: str | None = Field(default=None, max_length=50)

class CreateDirectChat(BaseModel):
    companion_id: int
    name: str | None = Field(default=None, max_length=30)
    description: str = Field(default=None, max_length=50)

class UpdateChat(BaseModel):
    name: str | None = Field(default=None, max_length=30)
    description: str = Field(max_length=50)

class CreateInvitation(BaseModel):
    user_id: int
    
class AcceptInvitation(BaseModel):
    id: int