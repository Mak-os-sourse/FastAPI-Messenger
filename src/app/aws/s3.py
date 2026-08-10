from aioboto3 import Session
from types_aiobotocore_s3 import S3Client


class S3:
    def __init__(self) -> None:
        self._session: Session = Session()
        self._s3: S3Client | None = None

    async def init(self, url: str, user: str, password: str) -> None:
        self._session = Session()
        self._s3 = await self._session.client(
            "s3",
            endpoint_url=url,
            use_ssl=False,
            aws_access_key_id=user,
            aws_secret_access_key=password,
        ).__aenter__()

    async def close(self) -> None:
        await self.client.__aexit__(None, None, None)

    @property
    def client(self) -> S3Client:
        if self._s3 is not None:
            return self._s3
        raise ValueError("The object S3 is not initialized, use init(...)")


s3 = S3()
