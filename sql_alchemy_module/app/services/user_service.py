from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..repositories.user_repository import UserRepository
from ..models.user import User


class UserNotFoundError(Exception):
    "User not found"

    pass


class UserService:
    def __init__(self, session: Session) -> None:
        self.users_repo = UserRepository(session)

    def register_new_user(
        self, full_name: str, email: str, phone_number: str
    ) -> dict[str, Any]:

        new_user = User(full_name=full_name, email=email, phone_number=phone_number)

        self.users_repo.create(new_user)

        self.users_repo.session.flush()

        return {
            "id": new_user.id,
            "full_name": new_user.full_name,
            "email": new_user.email,
            "phone_number": new_user.phone_number,
        }

    def get_user_by_id(self, id: int):
        user = self.users_repo.get_by_id(id)

        if user is None:
            raise UserNotFoundError(f"User with id: {id} not found")

        return user.to_dict()

    def delete_user_by_id(self, id: int):
        user = self.users_repo.get_by_id(id)
        if user is None:
            raise UserNotFoundError(f"User with id: {id} not found")

        user_dict = user.to_dict()

        self.users_repo.delete(user)

        return user_dict

    def get_all_users(self) -> list[dict[str, Any]]:
        stmt = select(User)

        users = self.users_repo.session.scalars(stmt).all()

        return [user.to_dict() for user in users]

    def update_user(self, user_id: int, data: dict[str, Any]) -> dict[str, Any]:
        user = self.users_repo.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(f"User with ID {user_id} does not exist.")

        user.full_name = str(data.get("full_name", user.full_name))
        user.email = str(data.get("email", user.email))
        user.phone_number = str(data.get("phone_number", user.phone_number))

        self.users_repo.save(user)
        return user.to_dict()
