import jwt

from typing import Any


class JWT_Manager:
    def __init__(self, secret: str, algorithm: str):
        self.secret = secret
        self.algorithm = algorithm

    def encode(self, data: dict[str, Any]):
        try:
            encoded = jwt.encode(data, self.secret, algorithm=self.algorithm)
            return encoded
        except Exception:
            return None

    def decode(self, token: str):
        try:
            decoded = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return decoded
        except Exception as e:
            print(e)
            return None
