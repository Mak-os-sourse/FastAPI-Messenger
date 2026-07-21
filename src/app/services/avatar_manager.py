from src.app.aws import S3Storage
from src.app.tasks.file import save_convert
from src.app.core.settings import settings

class AvatarManager:
    async def save(
        self, 
        storage: S3Storage, 
        id: int, 
        bucket: str,
        file: bytes, 
        input_format: str
    ) -> None:
        format = settings.file.base_image_format
        await storage.upload(
            file=file,
            bucket=bucket,
            key=f"avatar-{id}.{input_format}"
        )
        await save_convert.kiq(
            bucket=bucket,
            key=f"avatar-{id}.{input_format}",
            new_key=f"avatar-{id}-formatted.{format}"
        )
    
    async def get(self, storage: S3Storage, id: int):
        format = settings.file.base_image_format
        image = await storage.get(
            bucket=settings.s3.user_bucket,
            key=f"avatar-{id}-formatted.{format}",
        )
        return image

avatar_manager = AvatarManager()