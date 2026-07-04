from fastapi import HTTPException, status

class UnsupportedMediaType(HTTPException):
    def __init__(self, headers = None):
        super().__init__(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Unsupported media type", headers)