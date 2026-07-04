class FFmpegToolException(Exception):
    def __init__(self):
        super().__init__(f"File conversion error")