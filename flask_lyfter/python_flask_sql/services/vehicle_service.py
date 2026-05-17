import psycopg2
from typing import Any, Optional

from psycopg2.extensions import connection as _connection

from .service import BaseService
from ..repositories.vehicle_repository import Vehicle, VehicleRepository, VehicleStatus
from ..api.errors.vehicle_errors import (
    VehicleCreationError,
    VehicleDeletionError,
    VehicleDoesNotExistsError,
    VehicleUpdateError,
)

from ..api.errors.database_errors import DbRetrievalError, InvalidStatusError, InvalidFilterError


class VehicleService(BaseService):
    def __init__(self, db_conn: _connection) -> None:
        self.vehicle_repo = VehicleRepository(db_conn)

    def register(
        self,
        make: str,
        model: str,
        model_year: int,
        vehicle_status: Optional[VehicleStatus] = VehicleStatus.AVAILABLE,
    ) -> dict[str, Any]:

        new_vehicle: Vehicle | None = self.vehicle_repo.create(
            make, model, model_year, vehicle_status
        )

        if new_vehicle is None:
            raise VehicleCreationError("unable to create Vehicle")

        return new_vehicle.to_dict()

    def get(self, id: int) -> dict[str, Any]:
        try:
            vehicle = self.vehicle_repo.get_by_id(id)
            if vehicle is None:
                raise VehicleDoesNotExistsError(
                    f"vehicle with id: {id} does not exist in database"
                )
            return vehicle.to_dict()
        except Exception as e:
            print(f"get vehicle error: {e}")
            raise DbRetrievalError("unable to retrieve Vehicle ")

    def get_all(self, status: dict[str, str] | None) -> list[dict[str, Any]]:
        try:
            vehicles = self.vehicle_repo.get_all(status)
            if len(vehicles) < 1:
                raise VehicleDoesNotExistsError("vehicle list is empty")

            results: list[dict[str, Any]] = []
            for vehicle in vehicles:
                assert isinstance(vehicle, Vehicle)
                results.append(vehicle.to_dict())
            return results

        except ValueError:
            raise InvalidFilterError("invalid filter")
        except psycopg2.Error as pe:
            print(pe)
            raise DbRetrievalError("unable to retrieve vehicle")

    def delete(self, id: int):
        try:
            deleted_vehicle = self.vehicle_repo.delete(id)
            if deleted_vehicle is None:
                raise VehicleDoesNotExistsError(
                    f" Vehicle with id: {id} does not exist and cannot be deleted"
                )
            return deleted_vehicle.to_dict()
        except psycopg2.IntegrityError:
            raise VehicleDeletionError(
                "vehicle cannot be deleted due to active dependencies."
            )
        except VehicleDoesNotExistsError:
            raise
        except psycopg2.Error as e:
            print(f"Delete vehicle error: {e}")
            raise DbRetrievalError(
                f"internal database error during deletion of vehicle {id}"
            )

    def update_status(self, id: int, new_status: VehicleStatus):
        try:
            vehicle_status = None
            try:
                vehicle_status = VehicleStatus(new_status)
            except ValueError:
                raise InvalidStatusError(f"invalid status: {new_status}")

            db_vehicle_status = self.vehicle_repo.get_by_id(id)
            if not db_vehicle_status:
                raise VehicleDoesNotExistsError(
                    f"user with id: {id} does not exist and cannot be updated"
                )

            updated_vehicle = self.vehicle_repo.update_status(id, vehicle_status)

            if not updated_vehicle:
                raise VehicleUpdateError("unable to update vehicle in database")

            return updated_vehicle.to_dict()

        except VehicleDoesNotExistsError:
            raise
        except VehicleUpdateError:
            raise
