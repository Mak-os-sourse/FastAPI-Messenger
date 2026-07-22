from typing import Literal
from pydantic import BaseModel, Field

class ChatGroup(BaseModel):
    id: int
    type: Literal["public", "private"]
    name: str = Field(max_length=30)
    description: str | None = Field(max_length=50)
    admin_only: bool
    create_at: int

class ChatGroupResponse(ChatGroup):
    ...
    
class CreateGroupChat(BaseModel):
    type: Literal["public", "private"]
    name: str = Field(max_length=30)
    description: str | None = Field(default=None, max_length=50)
    admin_only: bool
    
class UpdateChat(BaseModel):
    name: str | None = Field(default=None, max_length=30)
    description: str | None = Field(default=None, max_length=50)
    admin_only: bool | None = None

class AcceptJoin(BaseModel):
    invitation_id: int
    is_admin: bool = False