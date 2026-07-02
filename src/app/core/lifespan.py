from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.app.models import *
from src.app.core.db import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.metadata_create_all()
    yield