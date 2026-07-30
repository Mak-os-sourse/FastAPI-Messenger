import magic
from fastapi import File, UploadFile

from app.core.settings import settings
from app.exc.file import UnsupportedMediaType


async def get_image(image: UploadFile = File()):
    format = magic.from_buffer(await image.read(), mime=True)
    if format not in settings.file.image_formats:
        raise UnsupportedMediaType()
    await image.seek(0)
    return image