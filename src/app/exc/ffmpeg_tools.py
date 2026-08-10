class FFmpegToolException(Exception):
    def __init__(self) -> None:
        super().__init__("Error convert")
