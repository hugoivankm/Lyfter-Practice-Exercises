import psycopg2
from psycopg2.extensions import connection as _connection
from typing import Any


from .service import BaseService
from .user_service import UserService
from .vehicle_service import VehicleService

from ..repositories.rental_repository import RentalRepository

from ..models.rental import RentalStatus
from ..models.user import AccountStatus
from ..models.vehicle import VehicleStatus

from ..api.errors.rental_errors import RentalCreationError, RentalDoesNotExistsError, RentalUpdateError
from ..api.errors.user_errors import UserDoesNotExistsError
from ..api.errors.vehicle_errors import VehicleDoesNotExistsError, VehicleUpdateError
from ..api.errors.database_errors import DbRetrievalError


class RentalService(BaseService):
    def __init__(self, db_conn: _connection) -> None:
        self.rental_repo = RentalRepository(db_conn)

        self._user_service = UserService(self.rental_repo.db)
        self._vehicle_service = VehicleService(self.rental_repo.db)

    def register(
        self,
        users_id: int,
        vehicles_id: int,
        status: RentalStatus = RentalStatus.PENDING,
    ):
        try:
            db_account_status = self._user_service.get(users_id).get("account_status")
            db_vehicle_status = self._vehicle_service.get(vehicles_id).get("vehicle_status")

            if db_account_status != AccountStatus.ACTIVE:
                raise RentalCreationError("user account must be in active status")
            if db_vehicle_status != VehicleStatus.AVAILABLE:
                raise RentalCreationError("vehicle must be available")

            new_rental = self.rental_repo.create(users_id, vehicles_id, status)

            if new_rental is None:
                raise RentalCreationError("unable to create Rental")

            return new_rental.to_dict()

        except (UserDoesNotExistsError, VehicleDoesNotExistsError) as e:
            raise RentalCreationError(str(e))
        except psycopg2.errors.CheckViolation:
            raise RentalCreationError(
                "failed to create rental with invalid account or user status"
            )
        except Exception as e:
            print(f"error: {e}")
            raise

    def complete_rental(self, rental_id: int) -> dict[str, Any]:
        try:
            rental = self.rental_repo.get_by_id(rental_id)
            if rental is None:
                 raise RentalUpdateError("Unable to retrieve rental")
            
            vehicle_id: int = rental.vehicles_id
            self._vehicle_service.update_status(vehicle_id, VehicleStatus.AVAILABLE)

            updated_rental = self.rental_repo.update_status(rental_id, RentalStatus.COMPLETED)
            if updated_rental is None:
                raise RentalUpdateError("Unable to update rental status")
            return updated_rental.to_dict()
            
        except psycopg2.Error as e:
            print(f"get rental error: {e}")
            raise DbRetrievalError("unable to retrieve rental from database")
        except VehicleUpdateError:
            raise RentalUpdateError("Unable to update vehicle status")
        except Exception as e:
            print(f"rental completion failed with error: {e}")
            raise


    def get(self, id: int) -> dict[str, Any]:
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

    def delete(self, id: int) -> None:
        raise NotImplementedError()
    
    def update_status(self, id: int, new_status: Any) -> dict[str, Any]:
        try:
            rental_status = None
            try:
                rental_status = RentalStatus(new_status)
            except ValueError:
                raise RentalUpdateError(f"Invalid status: {new_status}")

            db_user = self.rental_repo.get_by_id(id)
            if not db_user:
                raise RentalDoesNotExistsError(
                    f"Rental with id: {id} does not exist and cannot be updated"
                )

            updated_rental = self.rental_repo.update_status(id, rental_status)

            if not updated_rental:
                raise RentalUpdateError("Unable to update user in database")

            return updated_rental.to_dict()

        except UserDoesNotExistsError:
            raise
        except RentalUpdateError:
            raise
