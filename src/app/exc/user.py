from fastapi import HTTPException, status

class UserAlreadyExists(HTTPException):
    def __init__(self, headers = None):
        super().__init__(status.HTTP_409_CONFLICT, "User already exists", headers)

class Unauthorized(HTTPException):
    def __init__(self, headers = None):
        super().__init__(status.HTTP_401_UNAUTHORIZED, "User unauthorized", headers)

class UserNotFoud(HTTPException):
    def __init__(self, headers = None):
        super().__init__(status.HTTP_404_NOT_FOUND, "User not found", headers)
        