import pyotp, qrcode
from io import BytesIO

class Totp:
    def gen_secret_key(self) -> str:
        return pyotp.random_base32()
    
    def gen_uri(self, secret_key: str, username: str) -> str:
        totp = pyotp.TOTP(secret_key)
        return totp.provisioning_uri(name=username, issuer_name="Messager")
    
    def gen_qrcode(self, secret_key: str,username: str) -> str:
        """Return JPEG file"""
        buff = BytesIO()
        uri = self.gen_uri(secret_key, username)
        qrcode.make(uri).save(buff, format="    ")
        buff.seek(0)
        return buff.read()
    
    def verify(self, code: str | int, secret_key: str) -> bool:
        totp = pyotp.TOTP(secret_key)
        return totp.verify(str(code))
    
totp = Totp()