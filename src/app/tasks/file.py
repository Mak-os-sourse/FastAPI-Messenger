from src.app.services.ffmpeg_tools import ffmpeg_tools
from io import BytesIO

from src.app.core.task_broker import broker

@broker.task
async def convert(file: str | BytesIO | bytes,  output_format: str):
    ffmpeg_tools.convert(file=file, output_format=output_format)