from typing import Any

from sqlalchemy.orm import Session

from ..models.user import User
from ..repositories.user_repository import UserRepository


class UserNotFoundError(Exception):
    "User not found"



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

    def get_user_by_id(self, id: int, view: str = "compact") -> dict[str, Any]:
        user = self.users_repo.get_by_id(id)

        if user is None:
            raise UserNotFoundError(f"User with id: {id} not found")

        return user.to_dict(view=view)

    def delete_user_by_id(self, id: int) -> dict[str, Any]:
        user = self.users_repo.get_by_id(id)
        if user is None:
            raise UserNotFoundError(f"User with id: {id} not found")

        user_dict = user.to_dict()

        self.users_repo.delete(user)

        return user_dict

    def get_all_users(self, filter: str | None) -> list[dict[str, Any]]:
        if filter == "none":
            users = self.users_repo.get_by_vehicle_count(count=0, or_more=False)

        elif filter == "multiple":
            users = self.users_repo.get_by_vehicle_count(count=2, or_more=True)

        else:
            users = self.users_repo.get_by_vehicle_count(count=0, or_more=True)

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

    def get_users_by_vehicle_count(self, count: int = 0) -> list[dict[str, Any]]:
        users_by_count: list[User] = self.users_repo.get_by_vehicle_count(count)

        return [user.to_dict() for user in users_by_count]

    def get_users_with_more_vehicles_than(self, count: int = 1) -> list[dict[str, Any]]:
        users_by_count: list[User] = self.users_repo.get_by_vehicle_count(
            count, or_more=True
        )

        return [user.to_dict() for user in users_by_count]
