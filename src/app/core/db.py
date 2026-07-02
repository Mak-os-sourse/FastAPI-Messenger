from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import Pool

from src.app.core.settings import settings
from src.app.core.base import Base

class DB:
    def __init__(self, url: str, pool: Pool = None):
        self.engine = create_async_engine(url, pool=pool)
        self.sessionmaker = async_sessionmaker(self.engine)
    
    async def get_session(self):
        async with self.sessionmaker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
    
    async def metadata_create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
    async def metadata_drop_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

db = DB(settings.db.url)