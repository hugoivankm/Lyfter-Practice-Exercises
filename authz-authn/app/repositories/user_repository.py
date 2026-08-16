from app.models import User
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, username: str, password: str, role: str) -> User:
        user = User(username=username, password=password, role=role)
        self.session.add(user)
        self.session.flush() 
        return user

    def find_user(self, username: str, password: str) -> User | None:
        return (
            self.session.query(User)
            .filter(User.username == username, User.password == password)
            .first()
        )

    def find_user_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)
