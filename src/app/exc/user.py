from collections.abc import Mapping

from fastapi import HTTPException, status


class UserAlreadyExists(HTTPException):
    def __init__(self, headers: Mapping[str, str] | None = None) -> None:
        super().__init__(status.HTTP_409_CONFLICT, "User already exists", headers)


class Unauthorized(HTTPException):
    def __init__(self, headers: Mapping[str, str] | None = None):
        super().__init__(status.HTTP_401_UNAUTHORIZED, "User unauthorized", headers)


class UserNotFoud(HTTPException):
    def __init__(self, headers: Mapping[str, str] | None = None) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, "User not found", headers)
