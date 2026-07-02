from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    username: str = Field(min_length=4, max_length=15)
    name: str = Field(min_length=4, max_length=15)
    email: EmailStr
    description: str = Field(max_length=50)
    password: str = Field(min_length=6, max_length=60)
    create_at: int

class UserResponse(BaseModel):
    username: str = Field(min_length=4, max_length=15)
    name: str = Field(min_length=4, max_length=15)
    email: EmailStr
    description: str = Field(max_length=50)
    create_at: int