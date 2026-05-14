import psycopg2
from psycopg2.extensions import connection as _connection

from .service import BaseService
from .user_service import UserService
from .vehicle_service import VehicleService

from ..repositories.rental_repository import RentalRepository

from ..models.rental import Rental, RentalStatus
from ..models.user import AccountStatus
from ..models.vehicle import VehicleStatus

from ..api.errors.rental_errors import RentalCreationError
from ..api.errors.user_errors import UserDoesNotExistsError
from ..api.errors.vehicle_errors import VehicleDoesNotExistsError


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

    def get(self, id: int) -> Rental | None:
        raise NotImplementedError()

    def delete(self, id: int) -> None:
        raise NotImplementedError()
    
    def update_status(self, id: int, new_status: RentalStatus) -> None:
        raise NotImplementedError()
