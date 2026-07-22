from typing import Literal
from pydantic import BaseModel, Field

class Invitation(BaseModel):
    id: int
    chat_id: int
    user_id: int

class InvitationResponse(Invitation):
    ...

class CreateDirectChat(BaseModel):
    companion_id: int
    name: str | None = Field(default=None, max_length=30)
    description: str | None = Field(default=None, max_length=50)

class CreateInvitation(BaseModel):
    user_id: int
    
class AcceptInvitation(BaseModel):
    id: int