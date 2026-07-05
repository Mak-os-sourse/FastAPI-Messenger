from aioboto3 import Session
from types_aiobotocore_s3 import S3Client
from io import BytesIO

from src.app.core.settings import settings

import asyncio

class S3:
    def __init__(self, url: str):
        self.url = url
    
    async def init(self):
        self.session = Session()
        self.s3: S3Client = await self.session.resource("s3", endpoint_url=self.url).__aenter__()
        # self.upload()
    
    async def get(self, bucket: str, key: str) -> bytes:
        data = await self.s3.get_object(Backet=bucket, Key=key)
        return data["Body"].read()
    
    async def upload(self, bucket: str, key: str, file: str | bytes | BytesIO) -> None:
        await self.s3.put_object(file, Bucket=bucket, Key=key)
        
    async def delete(self, bucket: str, key: str) -> None:
        await self.s3.delete_object(Bucket=bucket, Key=key)

s3 = S3(settings.s3.url)

asyncio.run(s3.init())