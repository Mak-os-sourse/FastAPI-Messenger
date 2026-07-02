from fastapi import HTTPException, status

class InvalidToken(HTTPException):
    def __init__(self, headers = None):
        super().__init__(status.HTTP_403_FORBIDDEN, "Invalid token", headers)
        
class InvalidVerifyCode(HTTPException):
    def __init__(self, headers = None):
        super().__init__(status.HTTP_403_FORBIDDEN, "Invalid verify code", headers)
        