from typing import Any, Dict
from sqlalchemy.orm import Session
from app.utils.jwt_utils import JWTManager
from app.utils.security_utils import hash_password, verify_password
from app.models.user import User
from app.repositories import UserRepository


class UserService:
    def __init__(self, session: Session, jwt: JWTManager):
        self.repo = UserRepository(session)
        self.jwt = jwt

    def register(self, username: str, password: str) -> Dict[str, Any] | None:
        if self.repo.find_by_username(username):
            raise ValueError("Username already taken")

        hashed = hash_password(password)
        user = self.repo.create_user(username, hashed, role="standard")
        return self._build_token_response(user)

    def login(self, username: str, password: str) -> Dict[str, Any] | None:
        user = self.repo.find_by_username(username)
        if not user or not verify_password(password, user.password):
            return None
        return self._build_token_response(user)

    def get_by_id(self, id: int) -> User | None:
        return self.repo.find_user_by_id(id)

    def _build_token_response(self, user: User) -> dict[str, Any]:
        payload: Dict[str, Any] = {"sub": user.id, "role": user.role}
        access_data = self.jwt.encode_access_token(payload)
        refresh_data = self.jwt.encode_refresh_token(payload)

        return {
            "access_token": access_data["access_token"],
            "refresh_token": refresh_data["refresh_token"],
            "token_type": "Bearer",
            "expires_in": access_data["expires_in"],
        }
