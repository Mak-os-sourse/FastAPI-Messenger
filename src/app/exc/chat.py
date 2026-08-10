from collections.abc import Mapping

from fastapi import HTTPException, status


class ChatAlredyCreated(HTTPException):
    def __init__(self, headers: Mapping[str, str] | None = None):
        super().__init__(status.HTTP_409_CONFLICT, "Chat alredy created", headers)


class UserNotAdminInChat(HTTPException):
    def __init__(self, headers: Mapping[str, str] | None = None) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, "User not admin in chat", headers)


class InvitationNotFound(HTTPException):
    def __init__(self, headers: Mapping[str, str] | None = None) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, "Invitation not found", headers)


class ChatNotFound(HTTPException):
    def __init__(self, headers: Mapping[str, str] | None = None) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, "Chat not found", headers)
