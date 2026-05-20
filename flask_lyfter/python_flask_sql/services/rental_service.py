import psycopg2
from psycopg2.extensions import connection as _connection
from typing import Any, Optional

from .service import BaseService
from .user_service import UserService
from .vehicle_service import VehicleService

from ..repositories.rental_repository import Rental, RentalRepository

from ..models.rental import RentalStatus
from ..models.user import AccountStatus
from ..models.vehicle import VehicleStatus

from ..api.errors.rental_errors import (
    RentalCreationError,
    RentalDoesNotExistsError,
    RentalUpdateError,
)
from ..api.errors.user_errors import UserDoesNotExistsError
from ..api.errors.vehicle_errors import VehicleDoesNotExistsError, VehicleUpdateError
from ..api.errors.database_errors import DbRetrievalError, InvalidFilterError


class RentalService(BaseService):
    """Service layer for handling core transaction flows and business operations for Rentals.

    Coordinates activities between the RentalRepository and related domain services 
    (UserService, VehicleService) to ensure complex business constraints are met 
    before altering rental ledger states.

    Attributes:
        rental_repo (RentalRepository): Persistence layer abstraction for the rentals domain data store.
    """

    def __init__(self, db_conn: _connection) -> None:
        """Initializes the RentalService with downstream dependent service instances.

        Args:
            db_conn (_connection): An active psycopg2 database connection block.
        """
        self.rental_repo = RentalRepository(db_conn)

        # Sharing the exact same database transaction context context down the wire
        self._user_service = UserService(self.rental_repo.db)
        self._vehicle_service = VehicleService(self.rental_repo.db)

    def register(
        self,
        users_id: int,
        vehicles_id: int,
        status: RentalStatus = RentalStatus.PENDING,
    ) -> dict[str, Any]:
        """Registers a new vehicle rental transaction after validating business requirements.

        Validates that the target customer's account state is strictly ACTIVE and that 
        the target vehicle record context status is strictly AVAILABLE. Upon success, 
        automatically moves the target vehicle's state profile to RESERVED.

        Args:
            users_id (int): Unique database primary identifier key for the user.
            vehicles_id (int): Unique database primary identifier key for the vehicle.
            status (RentalStatus): The initial transactional status profile. 
                Defaults to RentalStatus.PENDING.

        Returns:
            dict[str, Any]: A structural dictionary layout tracking the newly opened rental record elements.

        Raises:
            RentalCreationError: If the target customer account isn't active, the vehicle isn't available, 
                relational data verification fails via Check Violations, or a downstream dependency fails.
            VehicleUpdateError: If the backend fails to safely toggle the vehicle context state to RESERVED.
        """
        try:
            db_account_status = self._user_service.get(users_id).get("account_status")
            db_vehicle_status = self._vehicle_service.get(vehicles_id).get(
                "vehicle_status"
            )

            if db_account_status != AccountStatus.ACTIVE:
                raise RentalCreationError("user account must be in active status")
            if db_vehicle_status != VehicleStatus.AVAILABLE:
                raise RentalCreationError("vehicle must be available")

            new_rental = self.rental_repo.create(users_id, vehicles_id, status)

            if new_rental is None:
                raise RentalCreationError("unable to create Rental")

            # update vehicle status
            _ = self._vehicle_service.update_status(vehicles_id, VehicleStatus.RESERVED)

            return new_rental.to_dict()

        except (UserDoesNotExistsError, VehicleDoesNotExistsError) as e:
            raise RentalCreationError(str(e))
        except psycopg2.errors.CheckViolation:
            raise RentalCreationError(
                "failed to create rental with invalid account or user status"
            )
        except VehicleUpdateError as e:
            print(f"Vehicle creation error: {e}")
            raise
        except Exception as e:
            print(f"error: {e}")
            raise

    def get(self, id: int) -> dict[str, Any]:
        """Retrieves a single transactional rental item matching a specific database entry key.

        Args:
            id (int): The unique integer row primary index identifier for the target rental record.

        Returns:
            dict[str, Any]: A serialized primitive mapping representation of the matching Rental.

        Raises:
            RentalDoesNotExistsError: If a lookup filter matches no structural entities in the data layer.
            DbRetrievalError: If connectivity failures or protocol drivers crash mid-transmission.
        """
        try:
            rental = self.rental_repo.get_by_id(id)
            if rental is None:
                raise RentalDoesNotExistsError(
                    f"rental with id: {id} does not exist in database"
                )
            return rental.to_dict()
        except psycopg2.Error as e:
            print(f"get rental error: {e}")
            raise DbRetrievalError("unable to retrieve rental")

    def get_all(self, status: dict[str, str] | None) -> list[dict[str, Any]]:
        """Queries and parses targeted collections of rental ledgers matching criteria parameters.

        Args:
            status (dict[str, str] | None): Dictionary key mappings holding query targets 
                and baseline match string data evaluated by dynamic query engines.

        Returns:
            list[dict[str, Any]]: A clean array data collection tracking individual dictionary 
                records. Returns an empty list if matching records result in a length less than 1.

        Raises:
            InvalidFilterError: If filtering parameters fail target dataclass whitelist matching layers.
            DbRetrievalError: On database infrastructure or statement layout mapping tracking loops errors.
        """
        try:
            rentals = self.rental_repo.get_all(status)
            if len(rentals) < 1:
                return []

            results: list[dict[str, Any]] = []
            for rental in rentals:
                assert isinstance(rental, Rental)
                results.append(rental.to_dict())
            return results

        except ValueError:
            raise InvalidFilterError("invalid filter")
        except psycopg2.Error:
            raise DbRetrievalError("unable to retrieve vehicle")

    def delete(self, id: int) -> None:
        """Removes an active rental record ledger entity directly out of database inventory arrays.

        Args:
            id (int): Unique reference index pointer tracking targeted columns.

        Raises:
            NotImplementedError: This functionality is explicitly disabled or unsupported in this iteration.
        """
        raise NotImplementedError()
    
    def _complete_rental(self, rental_id: int) -> Optional[Rental]:
        """Internal worker method processing state closing workflows for a completed rental.

        Frees up linked asset components by returning the targeted vehicle's data operational 
        state flag back to AVAILABLE before flipping the target rental state context flag to COMPLETED.

        Args:
            rental_id (int): The unique identification integer tracking the active rental sequence.

        Returns:
            Optional[Rental]: The updated Rental entity if the database commits status updates successfully.

        Raises:
            RentalUpdateError: If the vehicle resource update steps fail or if the repository 
                cannot commit the updated rental record.
            DbRetrievalError: On underlying relational row or connectivity driver socket processing drop exceptions.
        """
        try:
            rental = self.rental_repo.get_by_id(rental_id)
            if rental is None:
                raise RentalUpdateError("Unable to retrieve rental")

            vehicle_id: int = rental.vehicles_id
            v = self._vehicle_service.update_status(vehicle_id, VehicleStatus.AVAILABLE)
            print(v)

            updated_rental = self.rental_repo.update_status(
                rental_id, RentalStatus.COMPLETED
            )
            if updated_rental is None:
                raise RentalUpdateError("Unable to update rental status")
            
            return updated_rental

        except psycopg2.Error as e:
            print(f"get rental error: {e}")
            raise DbRetrievalError("unable to retrieve rental from database")
        except VehicleUpdateError:
            raise RentalUpdateError("Unable to update vehicle status")
        except Exception as e:
            print(f"rental completion failed with error: {e}")
            raise

    def update_status(self, id: int, new_status: Any) -> dict[str, Any]:
        """Updates the operational step state for a specific registered target rental ledger.

        Detects if the incoming processing target switches the transaction into a COMPLETED state. 
        If true, it routes tracking queries inward to trigger internal cross-service asset-release routines.

        Args:
            id (int): Unique tracking row integer mapping the specific rental identity records.
            new_status (Any): Target status context variable to evaluate (e.g., RentalStatus.COMPLETED).

        Returns:
            dict[str, Any]: A serialized dictionary representing the freshly updated status configurations.

        Raises:
            RentalUpdateError: If status argument parsing fails system requirements, if processing attempts 
                re-complete an already completed rental record, or if updates fail to register.
            RentalDoesNotExistsError: If early target lookup verification passes return null values.
        """
        try:
            rental_status = None
            try:
                rental_status = RentalStatus(new_status)
            except ValueError:
                raise RentalUpdateError(f"Invalid status: {new_status}")

            db_rental = self.rental_repo.get_by_id(id)
            if not db_rental:
                raise RentalDoesNotExistsError(
                    f"Rental with id: {id} does not exist and cannot be updated"
                )

            if new_status == RentalStatus.COMPLETED:
                if db_rental.rental_status == RentalStatus.COMPLETED:
                    raise RentalUpdateError("This rental has already been completed.")
                updated_rental = self._complete_rental(db_rental.id)
            else:
                updated_rental = self.rental_repo.update_status(id, rental_status)

            if not updated_rental:
                raise RentalUpdateError("Unable to update user in database")

            return updated_rental.to_dict()
        except DbRetrievalError:
            raise
        except UserDoesNotExistsError:
            raise
        except RentalUpdateError:
            raise