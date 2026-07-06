from ffmpeg.asyncio import FFmpeg
from io import BytesIO

from src.app.exc.ffmpeg_tools import FFmpegToolException

class FormatFile:
    png: str = "image2pipe"
    jpeg: str = "image2pipe"
    webp: str = "webp"
    mp4: str = "mp4"
    mkv: str = "matroska"
    webm: str = "webm"
    mov: str = "mov"
    mp3: str = "mp3"

class FFmpegTools:
    async def convert(
        self, file: str | BytesIO | bytes, 
        output_format: str,
    ) -> bytes:
        input_file = self._get_data_file(file)       
        ffmpeg = (
            FFmpeg().input("pipe:0")
            .output("pipe:1", format=output_format)
        )
        
        # out, _ = process.communicate(input=input_file)
        
        # if not out:
        #     raise FFmpegToolException()
        
        await ffmpeg.execute(input_file)
        
        # output = BytesIO(out)
        # return output.getvalue()
        
    def _get_data_file(self, file: str | BytesIO | bytes) -> bytes:
        if isinstance(file, BytesIO):
            return file.getvalue() 
        if isinstance(file, str):
            with open(file, "rb") as f:
                return f.read()
        else:
            return file
    
ffmpeg_tools = FFmpegTools()