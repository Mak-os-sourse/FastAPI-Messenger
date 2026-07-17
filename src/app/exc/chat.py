from fastapi import HTTPException, status

class UserNotAdminInChat(HTTPException):
    def __init__(self, headers = None):
        super().__init__(status.HTTP_403_FORBIDDEN, "User not admin in chat", headers)
        
class InvitationNotFound(HTTPException):
    def __init__(self, headers = None):
        super().__init__(status.HTTP_404_NOT_FOUND, "Invitation not found", headers)
        
class ChatNotFound(HTTPException):
    def __init__(self, headers = None):
        super().__init__(status.HTTP_404_NOT_FOUND, "Chat not found", headers)