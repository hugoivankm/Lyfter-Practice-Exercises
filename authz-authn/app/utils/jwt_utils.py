import jwt
import os
from typing import Any, Dict
from datetime import datetime, UTC, timedelta
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from dotenv import load_dotenv

load_dotenv()


class JWTManager:
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

    def _extract_subject(self, data: Dict[str, Any]) -> str:
        subject = data.get("sub") or data.get("user_id") or data.get("id")
        if subject is None:
            raise ValueError(
                "Payload must contain a user identifier (sub, user_id, or id)"
            )
        return str(subject)

    def _create_access_payload(
        self, data: Dict[str, Any], expires_in_minutes: int
    ) -> Dict[str, Any]:
        now = datetime.now(UTC)
        return {
            "sub": self._extract_subject(data),
            "role": data.get("role"),
            "type": "access",
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=expires_in_minutes)).timestamp()),
        }

    def _create_refresh_payload(
        self, data: Dict[str, Any], expires_in_days: int
    ) -> Dict[str, Any]:
        now = datetime.now(UTC)
        return {
            "sub": self._extract_subject(data),
            "role": data.get("role"),
            "type": "refresh",
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(days=expires_in_days)).timestamp()),
        }

    def encode_access_token(self, data: Dict[str, Any]) -> Dict[str, Any]:
        minutes = 15
        payload = self._create_access_payload(data, expires_in_minutes=minutes)
        token = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
        return {"access_token": token, "expires_in": minutes * 60}

    def encode_refresh_token(self, data: Dict[str, Any]) -> Dict[str, Any]:
        days = 7
        payload = self._create_refresh_payload(data, expires_in_days=days)
        token = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
        return {"refresh_token": token, "expires_in": days * 24 * 60 * 60}

    def decode(self, token: str) -> Dict[str, Any]:
        return jwt.decode(token, self.public_key, algorithms=[self.algorithm])
