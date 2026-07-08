import hashlib

from src.app.core.settings import settings

class Hash:
    def hash(self, data: str) -> str:
        string = data + settings.password.salt
        return hashlib.sha256(string.encode()).hexdigest()
    
    def verify(self, data: str, hash: str) -> bool:
        string = self.hash(data)
        return string == hash
    
hash_lib = Hash()