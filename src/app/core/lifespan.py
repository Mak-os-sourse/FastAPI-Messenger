from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.app.models import *
from src.app.aws.s3 import s3
from src.app.core.db import db
from src.app.core.cache import cache
from src.app.core.settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init(settings.db.url)
    cache.init(settings.redis.url)
    
    await s3.init(
        url=settings.s3.url,
        user=settings.s3.user,
        password=settings.s3.password,
    )
    await db.metadata_create_all()
    
    yield
    
    await cache.close()
    await s3.close()