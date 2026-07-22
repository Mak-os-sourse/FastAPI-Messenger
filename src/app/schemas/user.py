from typing import Literal
from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    id: int
    username: str = Field(min_length=4, max_length=30)
    name: str = Field(min_length=4, max_length=30)
    email: EmailStr
    description: str = Field(max_length=50)
    password: str = Field(min_length=6, max_length=60)
    create_at: int

class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    email: EmailStr
    description: str
    create_at: int

class UpdateData(BaseModel):
    name: str | None = Field(default=None, min_length=4, max_length=30)
    description: str | None = Field(default=None, max_length=50)
    type_status: Literal["online", "offline", "not-disturb"] | None = None

class Enable2FA(BaseModel):
    type: Literal["email", "totp"]
