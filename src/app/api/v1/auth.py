from fastapi import APIRouter, Body, Depends, Response, Cookie
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import Response
from redis.asyncio import Redis
from jwt import PyJWTError
from numpy import random
import time

from src.app.services.security import token, hash_lib, totp
from src.app.schemas.auth import (
    VerifyCode, LoginUser,
    LoginUserResponse, JwtToken,
    VerifyCodeResponse, CreateUser
)
from src.app.exc.user import UserNotFoud, UserAlreadyExists
from src.app.exc.auth import InvalidToken, InvalidVerifyCode
from src.app.core.settings import settings
from src.app.crud.user import user_crud
from src.app.deps.user import get_user
from src.app.deps.auth import security
from src.app.core.cache import cache
from src.app.models.user import User
from src.app.core.db import db

router = APIRouter(prefix="/auth")

@router.post("/update-token", response_model=JwtToken)
async def update_token(
    response: Response,
    refresh: str = Cookie(alias="token"),
    redis: Redis = Depends(cache.get_redis),    
    session: AsyncSession = Depends(db.get_session),
    access: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        access_key = f"{settings.redis.namespace}:token-blacklist:{access.credentials}:access"
        refresh_key = f"{settings.redis.namespace}:token-blacklist:{refresh}:refresh"
        
        refresh_data = token.decode(refresh)
        access_data = token.decode(access, verify_exp=False)
        
        if await redis.get(access_key) is not None:
            raise InvalidToken()
        if await redis.get(refresh_key) is not None:
            raise InvalidToken()      
        if refresh_data["id"] != access_data["id"]:
            raise InvalidToken()
        
        user = await user_crud.get_one(session, username=refresh_data["id"])
        if user is None:
            raise InvalidToken()
        
        now = time.time()
        await redis.set(refresh_key, None, ex=refresh_data["exp"] - now)
        
        refresh, access = token.create_tokens(id=user.id, username=user.username, email=user.email)
        response.set_cookie("token", refresh, httponly=True)
        
        return JwtToken(access=access) 
    except PyJWTError:
        raise InvalidToken()

@router.post("/regist", response_model=JwtToken)
async def regist_user(response: Response, user_data: CreateUser = Body(), session: AsyncSession = Depends(db.get_session)):
    user = await user_crud.get_one(session, username=user_data.username)
    if user is not None:
        raise UserAlreadyExists()
    
    password = hash_lib.hash(user_data.password)
    
    user = await user_crud.add(
        session,
        username=user_data.username,
        name=user_data.name,
        email=user_data.email,
        password=password,
        description=user_data.description,
    )
    
    refresh, access = token.create_tokens(id=user.id, username=user.username, email=user.email)
    response.set_cookie("token", refresh, httponly=True)
    
    return JwtToken(access_token=access)

@router.post("/login", response_model=LoginUserResponse)
async def login_user(
    response: Response,
    user_data: LoginUser = Body(),
    session: AsyncSession = Depends(db.get_session)
):
    user = await user_crud.get_one(session, username=user_data.username)
    if user is None:
        raise UserNotFoud()
    
    if hash_lib.verify(user_data.password, user.password):
        if user.type_2fa is not None:
            return LoginUserResponse(user_id=user.id, type_2fa=user.type_2fa)
        else:                
            refresh, access = token.create_tokens(username=user_data.username, email=user_data.email)
            response.set_cookie("token", refresh, httponly=True)
            
            return LoginUserResponse(access=access, user_id=user.id)
    
@router.post("/verify-code/gen", response_model=VerifyCodeResponse)
async def gen_code(
    user: User = Depends(get_user),
    redis: Redis = Depends(cache.get_redis),
):
    for _ in range(100):
        code = random.randint(100000, 999999)
        key = f"{settings.redis.namespace}:verify-code:user:{user.id}:id"
        
        if await redis.get(key) is None:
            await redis.set(key, code)
            # email.send bla bla bla
            return VerifyCodeResponse(send_code=True)

@router.post("/verify-code/verify", response_model=JwtToken)
async def code_verify(
    response: Response,
    verify_code: VerifyCode = Body(),
    user: User = Depends(get_user),
    redis: Redis = Depends(cache.get_redis),
):
    key = f"{settings.redis.namespace}:verify-code:user:{user.id}:id"
    code = await redis.get(key)
    if code == verify_code.code:
        refresh, access = token.create_tokens(username=user.username, email=user.email)
        response.set_cookie("token", refresh, httponly=True)
                
        return JwtToken(access_token=access)
    else:
        raise InvalidVerifyCode()
    
@router.post("/opt/gen-qrcode")
async def gen_qrcode(
    user: User = Depends(get_user),
):
    qrcode = totp.gen_qrcode(user.secret_key, user.username)
    return Response(qrcode, media_type="image/jpeg")

@router.post("otp/verify", response_model=JwtToken)
async def otp_verify(
    response: Response,
    verify_code: VerifyCode = Body(),
    user: User = Depends(get_user),
):
    if totp.verify(verify_code.code, user.secret_key):
        refresh, access = token.create_tokens(username=user.username, email=user.email)
        response.set_cookie("token", refresh, httponly=True)
                
        return JwtToken(access_token=access)
    else:
        raise InvalidVerifyCode()
    
@router.post("/logout")
async def logout(
    response: Response,
    refresh: str = Cookie(alias="token"),
    redis: Redis = Depends(cache.get_redis),
    access: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        access_key = f"{settings.redis.namespace}:token-blacklist:{access.credentials}:access"
        refresh_key = f"{settings.redis.namespace}:token-blacklist:{refresh}:refresh"
        
        refresh_data = token.decode(refresh)
        access_data = token.decode(access)
        
        if refresh_data["id"] != access_data["id"]:
            raise InvalidToken()
        
        now = time.time()
        redis.set(access_key, None, ex=access_data["exp"] - now)
        redis.set(refresh_key, None, ex=refresh_data["exp"] - now)
        response.delete_cookie("token")
    except PyJWTError:
        raise InvalidToken()