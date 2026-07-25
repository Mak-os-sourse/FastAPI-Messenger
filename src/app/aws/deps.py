from app.aws.s3 import s3
from app.aws.s3_storage import S3Storage

async def get_storage():
    return S3Storage(s3.client)