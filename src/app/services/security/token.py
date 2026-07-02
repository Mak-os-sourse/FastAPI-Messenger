import jwt
import time

from src.app.core.settings import settings

class Token:
    def create_tokens(self, id: int,  username: str, email: str) -> tuple[str, str]:
        """Use refresh, access = token.create(...)"""
        now = int(time.time())
        refresh_exp = now + settings.jwt.refresh_exp
        access_exp = now + settings.jwt.access_exp
        
        refresh = self.encode(id, username, email, exp=refresh_exp)
        access = self.encode(id, username, email, exp=access_exp)
        return refresh, access
    
    def encode(self, id: int, username: str, email: str, exp: int) -> str:
        return jwt.encode(
            {
                "id": id,
                "username": username,
                "email": email,
                "exp": exp,
            },
            key=settings.jwt.key,
            algorithm=settings.jwt.algorithm,
        )
    
    def decode(self, token: str, verify_exp: bool = True) -> dict:
        return jwt.decode(
            token,
            key=settings.jwt.key,
            algorithms=settings.jwt.algorithm,
            options={"verify_exp": verify_exp}
        )
        
token = Token()