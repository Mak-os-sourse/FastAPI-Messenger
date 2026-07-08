from pydantic import BaseModel, Field, EmailStr

class JwtToken(BaseModel):
    access_token: str
    token_type: str = "bearer"

class CreateUser(BaseModel):
    username: str = Field(min_length=4, max_length=30)
    name: str = Field(min_length=4, max_length=30)
    email: EmailStr
    description: str = Field(max_length=50)
    password: str = Field(min_length=6, max_length=15)

class LoginUser(BaseModel):
    username: str = Field(min_length=4, max_length=30)
    password: str = Field(min_length=6, max_length=16)
    
class LoginUserResponse(BaseModel):
    user_id: int
    access_token: str = None
    enable_2fa: bool = True

class VerifyCodeResponse(BaseModel):
    send_code: bool

class VerifyCode(BaseModel):
    code: int