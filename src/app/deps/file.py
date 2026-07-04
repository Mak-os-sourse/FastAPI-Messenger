import magic
from fastapi import UploadFile, File

from src.app.exc.file import UnsupportedMediaType
from src.app.core.settings import settings

async def get_image(image: UploadFile = File()):
    format = magic.from_buffer("test.jpeg", mime=True)
    if format not in settings.file.image_formats:
        raise UnsupportedMediaType()
    return image