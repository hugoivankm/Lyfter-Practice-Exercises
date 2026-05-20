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

            # update vechicle status
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
        raise NotImplementedError()
    
    def _complete_rental(self, rental_id: int) -> Optional[Rental]:
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
