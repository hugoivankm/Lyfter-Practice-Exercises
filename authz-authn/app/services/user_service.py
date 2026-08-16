from sqlalchemy.orm import Session
from app.utils.jwt_utils import JWT_Manager
from app.models.user import User
from app.repositories import UserRepository


class UserService:
    def __init__(self, session: Session, jwt: JWT_Manager):
        self.repo = UserRepository(session)
        self.jwt = jwt

    def register(self, username: str, password: str) -> str | None:
        user = self.repo.create_user(
            username,
            password,
            role="standard"
            )
        return self.jwt.encode({"id": user.id, "role": user.role})

    def login(self, username: str, password: str) -> str | None:
        user = self.repo.find_user(username, password)
        if not user:
            return None
        return self.jwt.encode({"id": user.id, "role": user.role})

    def get_by_id(self, id: int) -> User | None:
        return self.repo.find_user_by_id(id)
