import base64

from app.core.settings import settings
from app.tasks.file import save_convert


class AvatarManager:
    async def save(self, id: int | str, bucket: str, file: bytes, input_format: str) -> None:
        format = settings.file.base_image_format
        buff = base64.b64encode(file).decode()

        await save_convert.kiq(
            file=buff,
            key=f"avatar-{id}.{input_format}",
            new_key=f"avatar-{id}.{format}",
            bucket=bucket,
        )

    def get_url_file(self, id: int, bucket: str) -> str:
        format = settings.file.base_image_format
        url_s3 = settings.s3.url
        if url_s3[-1] != "/":
            url_s3 += "/"
        return f"{url_s3}{bucket}/avatar-{id}.{format}"


avatar_manager = AvatarManager()
