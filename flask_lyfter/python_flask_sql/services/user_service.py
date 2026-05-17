from datetime import date
from typing import Any

import psycopg2
from psycopg2.extensions import connection as _connection

from .service import BaseService
from ..repositories.user_repository import UserRepository
from ..models.user import User, AccountStatus
from ..api.errors.user_errors import (
    UserCreationError,
    UserDeletionError,
    UserDoesNotExistsError,
    UserUpdateError,
    AlreadyExistsError,
)

from  ..api.errors.database_errors import DbRetrievalError, InvalidFilterError


class UserService(BaseService):
    def __init__(self, db_conn: _connection) -> None:
        self.user_repo = UserRepository(db_conn)

    def register(
        self,
        email: str,
        username: str,
        password: str,
        birthdate: date,
        account_status: AccountStatus = AccountStatus.ACTIVE,
    ):
        try:
            new_user: User | None = self.user_repo.create(
                email, username, password, birthdate, account_status
            )
            if new_user is None:
                raise UserCreationError("unable to create user")

            return new_user.to_dict()
        except psycopg2.errors.UniqueViolation:
            raise AlreadyExistsError("user email or username already exists")
        except psycopg2.errors.CheckViolation:
            raise UserCreationError("failed to create user with invalid account status")

    def get(self, id: int):
        try:
            user = self.user_repo.get_by_id(id)
            if user is None:
                raise UserDoesNotExistsError(
                    f"user with id: {id} does not exist in database"
                )
            return user.to_dict()
        except psycopg2.Error as e:
            print(f"get user error: {e}")
            raise DbRetrievalError("unable to retrieve user")
        
    def get_all(self, status: dict[str, str] | None) -> list[dict[str, Any]]:
        try:
            users = self.user_repo.get_all(status)
            if len(users) < 1:
                raise UserDoesNotExistsError("user vehicle list is empty")

            results: list[dict[str, Any]] = []
            for user in users:
                assert isinstance(user, User)
                results.append(user.to_dict())
            return results
        
        except ValueError:
            raise InvalidFilterError("invalid filter")
        except psycopg2.Error:
            raise DbRetrievalError("unable to retrieve vehicle")

    def delete(self, id: int):
        try:
            deleted_user = self.user_repo.delete(id)

            if deleted_user is None:
                raise UserDoesNotExistsError(
                    f"user with id: {id} does not exist and cannot be deleted"
                )

            return deleted_user.to_dict()

        except psycopg2.IntegrityError:
            raise UserDeletionError(
                "user cannot be deleted due to active dependencies."
            )
        except UserDoesNotExistsError:
            raise
        except psycopg2.Error as e:
            print(f"Delete user error: {e}")
            raise DbRetrievalError(
                f"internal database error during deletion of user {id}"
            )

    def update_status(self, id: int, new_status: AccountStatus):
        try:
            account_status = None
            try:
                account_status = AccountStatus(new_status)
            except ValueError:
                raise UserUpdateError(f"Invalid status: {new_status}")

            db_user = self.user_repo.get_by_id(id)
            if not db_user:
                raise UserDoesNotExistsError(
                    f"user with id: {id} does not exist and cannot be updated"
                )

            updated_user = self.user_repo.update_status(id, account_status)

            if not updated_user:
                raise UserUpdateError("unable to update user in database")

            return updated_user.to_dict()

        except UserDoesNotExistsError:
            raise
        except UserUpdateError:
            raise
