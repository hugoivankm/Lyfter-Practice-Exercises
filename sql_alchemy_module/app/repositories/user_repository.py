from typing import Optional
from sqlalchemy.orm import Session
from app.models import User

class UserRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)

    def create(self, user: User) -> User:
        self.session.add(user)
        return user

    def delete(self, user: User):
        self.session.delete(user)

    def save(self, user: User) -> User:
        self.session.add(user)
        return user
