from sqlalchemy.orm import Session

from app.models import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, username: str, password_hash: str, role: str) -> User:
        user = User(username=username, password=password_hash, role=role)
        self.session.add(user)
        self.session.flush()
        return user

    def find_by_username(self, username: str) -> User | None:
        return self.session.query(User).filter(User.username == username).first()

    def find_user_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)
