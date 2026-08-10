from app.aws.deps import get_storage
from app.aws.s3 import s3
from app.aws.s3_storage import S3Storage

__all__ = [
    "S3Storage",
    "get_storage",
    "s3",
]
