from datetime import date

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
from flask_lyfter.python_flask_sql.api.errors.database_errors import DbRetrievalError


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

    def get(self, user_id: int):
        try:
            user = self.user_repo.get_by_id(user_id)
            if user is None:
                raise UserDoesNotExistsError(
                    f"user with id: {user_id} does not exist in database"
                )
            return user.to_dict()
        except psycopg2.Error as e:
            print(f"get user error: {e}")
            raise DbRetrievalError("unable to retrieve user")

    def delete(self, user_id: int):
        try:
            deleted_user = self.user_repo.delete(user_id)

            if deleted_user is None:
                raise UserDoesNotExistsError(
                    f"User with id: {user_id} does not exist and cannot be deleted"
                )

            return deleted_user.to_dict()

        except psycopg2.IntegrityError:
            raise UserDeletionError(
                "User cannot be deleted due to active dependencies."
            )
        except UserDoesNotExistsError:
            raise
        except psycopg2.Error as e:
            print(f"Delete user error: {e}")
            raise DbRetrievalError(
                f"Internal database error during deletion of user {user_id}"
            )

    def update_status(self, user_id: int, new_status: AccountStatus):
        try:
            account_status = None
            try:
                account_status = AccountStatus(new_status)
            except ValueError:
                raise UserUpdateError(f"Invalid status: {new_status}")

            db_user = self.user_repo.get_by_id(user_id)
            if not db_user:
                raise UserDoesNotExistsError(
                    f"User with id: {user_id} does not exist and cannot be updated"
                )

            updated_user = self.user_repo.update_status(user_id, account_status)

            if not updated_user:
                raise UserUpdateError("Unable to update user in database")

            return updated_user.to_dict()

        except UserDoesNotExistsError:
            raise
        except UserUpdateError:
            raise
