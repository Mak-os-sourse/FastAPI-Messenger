from collections.abc import Mapping

from fastapi import HTTPException, status

from app.websocket.tools import WebSocketError


class WSInvalidToken(WebSocketError):
    def __init__(self) -> None:
        super().__init__("InvalidToken", "Invalid token")


class InvalidToken(HTTPException):
    def __init__(self, headers: Mapping[str, str] | None = None) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, "Invalid token", headers)


class InvalidVerifyCode(HTTPException):
    def __init__(self, headers: Mapping[str, str] | None = None) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, "Invalid verify code", headers)


class NotEnable2FA(HTTPException):
    def __init__(self, headers: Mapping[str, str] | None = None) -> None:
        super().__init__(status.HTTP_409_CONFLICT, "Not enable 2FA", headers)


class Unauthorized(HTTPException):
    def __init__(self, headers: Mapping[str, str] | None = None) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, "Unauthorized", headers)


class ErrorGenCode(HTTPException):
    def __init__(self, headers: Mapping[str, str] | None = None) -> None:
        super().__init__(status.HTTP_409_CONFLICT, "No gen code", headers)
