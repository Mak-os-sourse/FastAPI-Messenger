from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

class DBSettings(BaseModel):
    url: str

class RedisSettings(BaseModel):
    url: str
    namespace: str

class JWTSettings(BaseModel):
    key: str
    algorithm: str
    refresh_exp: int
    access_exp: int

class PasswordSettings(BaseModel):
    salt: str

class VerifyCodeSettings(BaseModel):
    interval: int

class FileSettings(BaseModel):
    image_formats: list[str]

class Settings(BaseSettings):
    db: DBSettings
    redis: RedisSettings
    jwt: JWTSettings
    password: PasswordSettings
    verify_code: VerifyCodeSettings
    file: FileSettings
    
    model_config = SettingsConfigDict(env_file="settings.env", env_nested_delimiter="__")
    
settings = Settings()