from collections.abc import Mapping

from fastapi import HTTPException, status


class UnsupportedMediaFormat(Exception):
    def __init__(self) -> None:
        super().__init__("Unsupported media format")


class UnsupportedMediaType(HTTPException):
    def __init__(self, headers: Mapping[str, str] | None = None) -> None:
        super().__init__(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Unsupported media type", headers)
