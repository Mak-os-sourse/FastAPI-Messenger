from types_aiobotocore_s3 import S3Client
from io import BytesIO

class S3Storage:
    def __init__(self, client: S3Client):
        self.client = client
        
    async def get(self, bucket: str, key: str) -> bytes:
        data = await self.client.get_object(Bucket=bucket, Key=key)
        return await data["Body"].read()
    
    async def upload(self, bucket: str, key: str, file: str | bytes | BytesIO) -> None:
        if isinstance(file, str):
            with open(file, "rb") as f:
                file = f.read()
        await self.client.put_object(Body=file, Bucket=bucket, Key=key)
        
    async def delete(self, bucket: str, key: str) -> None:
        await self.client.delete_object(Bucket=bucket, Key=key)
