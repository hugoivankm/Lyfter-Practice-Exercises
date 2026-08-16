import jwt
import os
from typing import Any
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from dotenv import load_dotenv

load_dotenv()


class JWT_Manager:
    def __init__(self, algorithm: str = "RS256"):
        self.algorithm = algorithm

        private_key_path = os.getenv(
            "JWT_PRIVATE_KEY_PATH", "./secrets/private_key.pem"
        )
        public_key_path = os.getenv("JWT_PUBLIC_KEY_PATH", "./secrets/public_key.pem")

        os.makedirs(os.path.dirname(os.path.abspath(private_key_path)), exist_ok=True)
        os.makedirs(os.path.dirname(os.path.abspath(public_key_path)), exist_ok=True)

        keys_exist = (
            os.path.exists(private_key_path)
            and os.path.getsize(private_key_path) > 0
            and os.path.exists(public_key_path)
            and os.path.getsize(public_key_path) > 0
        )

        if keys_exist:
            try:
                with open(private_key_path, "rb") as f:
                    self.private_key = f.read()

                with open(public_key_path, "rb") as f:
                    self.public_key = f.read()
                return  
            except Exception as e:
                print(f"Error loading existing keys: {e}. Generating new key pair...")

        private_key_obj = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        self.private_key = private_key_obj.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        self.public_key = private_key_obj.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        with open(private_key_path, "wb") as f:
            f.write(self.private_key)

        with open(public_key_path, "wb") as f:
            f.write(self.public_key)

    def encode(self, data: dict[str, Any]):
        try:
            encoded = jwt.encode(data, self.private_key, algorithm=self.algorithm)
            return encoded
        except Exception:
            return None

    def decode(self, token: str):
        try:
            decoded = jwt.decode(token, self.public_key, algorithms=[self.algorithm])
            return decoded
        except Exception as e:
            print(e)
            return None