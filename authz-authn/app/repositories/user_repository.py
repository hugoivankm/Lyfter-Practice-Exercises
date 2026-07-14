from app.models.user import User
from app.database.db_manager import DatabaseManager


class UserRepository:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def create_user(self, username: str, password: str) -> User:
        with self.db.session() as session:
            user = User(username=username, password=password)
            session.add(user)
            session.flush()  # ensure buffer gets flushed in time
            return user

    def find_user(self, username: str, password: str) -> User | None:
        with self.db.session() as session:
            return (
                session.query(User)
                .filter(User.username == username, User.password == password)
                .first()
            )

    def find_user_by_id(self, user_id: int) -> User | None:
        with self.db.session() as session:
            return session.query(User).filter(User.id == user_id).first()