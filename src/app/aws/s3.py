from aioboto3 import Session
from types_aiobotocore_s3 import S3Client

class S3:
    async def init(self, url: str, user: str, password: str):
        self._session = Session()
        self._s3: S3Client = await self._session.client(
            "s3",
            endpoint_url=url,
            use_ssl=False,
            aws_access_key_id=user,
            aws_secret_access_key=password,
        ).__aenter__()
        
    async def close(self):
        await self._s3.__aexit__()
        
    @property
    def client(self):
        return self._s3
    
s3 = S3()