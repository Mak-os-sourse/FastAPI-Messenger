import base64

from src.app.aws import S3Storage
from src.app.tasks.file import save_convert
from src.app.core.settings import settings

class AvatarManager:
    async def save(
        self, 
        id: int | str, 
        bucket: str,
        file: bytes, 
        input_format: str
    ) -> None:
        format = settings.file.base_image_format
        buff = base64.b64encode(file).decode()
        
        await save_convert.kiq(
            file=buff,
            bucket=bucket,
            key=f"avatar-{id}.{input_format}",
            new_key=f"avatar-{id}.{format}"
        )
    
    async def get(self, storage: S3Storage, id: int | str):
        format = settings.file.base_image_format
        image = await storage.get(
            bucket=settings.s3.user_bucket,
            key=f"avatar-{id}.{format}",
        )
        return image

avatar_manager = AvatarManager()