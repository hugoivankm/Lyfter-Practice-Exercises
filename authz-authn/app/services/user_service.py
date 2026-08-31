from typing import Any

from app.models.user import User
from app.repositories import UserRepository
from app.services.login_entry_service import LoginEntryService
from app.utils.jwt_utils import JWTManager
from app.utils.security_utils import hash_password, verify_password
from sqlalchemy.orm import Session


class UserService:
    def __init__(self, session: Session):
        self.repo = UserRepository(session)
        self.loginEntryService = LoginEntryService(session)

    def register(
        self, username: str, password: str, jwt: JWTManager
    ) -> dict[str, Any] | None:
        if self.repo.find_by_username(username):
            raise ValueError("Username already taken")

        hashed = hash_password(password)
        user = self.repo.create_user(username, hashed, role="standard")
        return self._build_token_response(user)

    def login(
        self,
        jwt: JWTManager,
        username: str,
        password: str,
        ip_address: str | None = None,
    ) -> dict[str, Any] | None:
        user = self.repo.find_by_username(username)

        if user is None:
            self.loginEntryService.record_entry(
                user_id=None, is_success=False, ip_address=ip_address
            )
            return None

        if not verify_password(password, user.password):
            self.loginEntryService.record_entry(
                user_id=user.id, is_success=False, ip_address=ip_address
            )
            return None

        self.loginEntryService.record_entry(
            user_id=user.id, is_success=True, ip_address=ip_address
        )

        return self._build_token_response(user, jwt)

    def get_by_id(self, id: int) -> User | None:
        return self.repo.find_user_by_id(id)

    def _build_token_response(self, user: User, jwt: JWTManager) -> dict[str, Any]:
        payload: dict[str, Any] = {"sub": user.id, "role": user.role}
        access_data = jwt.encode_access_token(payload)
        refresh_data = jwt.encode_refresh_token(payload)

        return {
            "access_token": access_data["access_token"],
            "refresh_token": refresh_data["refresh_token"],
            "token_type": "Bearer",
            "expires_in": access_data["expires_in"],
        }
