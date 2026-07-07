from io import BytesIO
from taskiq import TaskiqDepends

from src.app.core.task_broker import broker
from src.app.aws import get_storage, S3Storage
from src.app.services.ffmpeg_tools import ffmpeg_tools, FormatFile

@broker.task
async def save_convert(
    file: str | BytesIO | bytes,
    bucket: str,
    key: str,
    storage: S3Storage = TaskiqDepends(get_storage),
):
    format_file = key.split(".")[-1]
    format = getattr(FormatFile, format_file, None)
    if format is None:
        raise # bla bla bla
    data = await ffmpeg_tools.convert(file=file, output_format=format)
    await storage.upload(bucket=bucket, key=key, file=data)