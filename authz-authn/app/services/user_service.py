from app.repositories.user_repository import UserRepository
from app.utils.jwt_utils import JWT_Manager
from app.models.user import User


class UserService:
    def __init__(self, repo: UserRepository, jwt: JWT_Manager):
        self.repo = repo
        self.jwt = jwt

    def register(self, username: str, password: str) -> str | None:
        user = self.repo.create_user(username, password)
        return self.jwt.encode({"id": user.id})

    def login(self, username: str, password: str) -> str | None:
        user = self.repo.find_user(username, password)
        if not user:
            return None
        return self.jwt.encode({"id": user.id})

    def get_user_from_token(self, token: str) -> User | None:
        decoded = self.jwt.decode(token)
        if not decoded:
            return None
        return self.repo.find_user_by_id(decoded["id"])
