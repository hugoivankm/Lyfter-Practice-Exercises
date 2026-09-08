from datetime import date
from typing import Any

import psycopg2
from psycopg2.extensions import connection as _connection

from ..api.errors.database_errors import DbRetrievalError, InvalidFilterError
from ..api.errors.user_errors import (
    AlreadyExistsError,
    UserCreationError,
    UserDeletionError,
    UserDoesNotExistsError,
    UserUpdateError,
)
from ..models.user import AccountStatus, User
from ..repositories.user_repository import UserRepository
from .service import BaseService


class UserService(BaseService):
    """Service layer for handling core domain logic and workflows for Users.

    Acts as the orchestrator for user administration, authentication support structures,
    account creation constraints, status transitions, and data extraction pipelines.

    Attributes:
        user_repo (UserRepository): Data repository abstraction layer for managing database persistence.
    """

    def __init__(self, db_conn: _connection) -> None:
        """Initializes the UserService with an active database connection.

        Args:
            db_conn (_connection): A live psycopg2 database connection.
        """
        self.user_repo = UserRepository(db_conn)

    def register(
        self,
        email: str,
        username: str,
        password: str,
        birthdate: date,
        full_name: str,
        account_status: AccountStatus = AccountStatus.ACTIVE,
    ) -> dict[str, Any]:
        """Registers a brand new user within the system identity platform.

        Args:
            email (str): Unique communication email address for the user profile.
            username (str): Unique identifying moniker selected by the user.
            password (str): Encrypted credential string representing access keys.
            birthdate (date): Calendar birth date instance used for age validation criteria.
            account_status (AccountStatus): Initial operational state. Defaults to AccountStatus.ACTIVE.

        Returns:
            dict[str, Any]: A dictionary representation of the newly created User entity data.

        Raises:
            AlreadyExistsError: If the specified email or username values violate database unique constraints.
            UserCreationError: If data values violate explicit relational table check conditions
                or if the internal repository pipeline execution returns a null profile state.
        """
        try:
            new_user: User | None = self.user_repo.create(
                email, username, password, birthdate, full_name, account_status
            )
            if new_user is None:
                raise UserCreationError("unable to create user")

            return new_user.to_dict()
        except psycopg2.errors.UniqueViolation:
            raise AlreadyExistsError("user email or username already exists")
        except psycopg2.errors.CheckViolation:
            raise UserCreationError("failed to create user with invalid account status")

    def get(self, id: int) -> dict[str, Any]:
        """Retrieves a single user profile record via its primary unique database index.

        Args:
            id (int): Unique target identity integer reference tracking key.

        Returns:
            dict[str, Any]: A serialized dictionary representing the targeted user attributes.

        Raises:
            UserDoesNotExistsError: If no data record row matches the provided identifier.
            DbRetrievalError: If underlying low-level database socket connection faults occur
                during operational query transmission.
        """
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
        """Queries and returns matching arrays of user profiles leveraging arbitrary structural filter properties.

        Args:
            status (dict[str, str] | None): Dictionary key-value attributes matching columns
                and runtime string values used to structure WHERE blocks dynamically.

        Returns:
            list[dict[str, Any]]: A list of plain dictionary structures representing every
                matching user profile matching the target parameters.

        Raises:
            UserDoesNotExistsError: If execution outputs match zero items or collection length indicates zero items.
            InvalidFilterError: If input key maps fail metadata dataclass reflection validation logic.
            DbRetrievalError: On internal engine errors or driver operational faults encountered
                during loop parsing.
        """
        try:
            users = self.user_repo.get_all(status)
            if len(users) < 1:
                return []

            results: list[dict[str, Any]] = []
            for user in users:
                assert isinstance(user, User)
                results.append(user.to_dict())
            return results

        except ValueError:
            raise InvalidFilterError("invalid filter")
        except psycopg2.Error:
            raise DbRetrievalError("unable to retrieve vehicle")

    def delete(self, id: int) -> dict[str, Any]:
        """Removes an existing user profile record entirely out of active database operations.

        Args:
            id (int): The unique integer database ID tracking the profile to purge.

        Returns:
            dict[str, Any]: A historical dictionary object containing properties of the
                purged target record for confirmation logs.

        Raises:
            UserDoesNotExistsError: If a verification check finds no target user matching the key.
            UserDeletionError: If relational parent-child barriers block removal due to existing active
                dependencies (e.g., historical user accounts with linked active rental records).
            DbRetrievalError: On systemic transactional connection failures or driver errors.
        """
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

    def update_status(self, id: int, new_status: AccountStatus) -> dict[str, Any]:
        """Transitions a target user account configuration into a new system operational status.

        Args:
            id (int): The unique database reference tracking identifier for the user profile.
            new_status (AccountStatus): The target status enum value (e.g., AccountStatus.SUSPENDED,
                AccountStatus.ACTIVE) to transition into.

        Returns:
            dict[str, Any]: A serialized dictionary reflecting the modified profile status schema.

        Raises:
            UserUpdateError: If input status properties cannot resolve to a valid system enum
                or if statements post-processing returns empty result structures.
            UserDoesNotExistsError: If a validation lookup query shows the target profile ID row
                does not exist.
        """
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
