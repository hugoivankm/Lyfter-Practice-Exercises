from typing import Any, Optional

import psycopg2
from psycopg2.extensions import connection as _connection

from .service import BaseService
from ..repositories.vehicle_repository import Vehicle, VehicleRepository, VehicleStatus
from ..api.errors.vehicle_errors import (
    VehicleCreationError,
    VehicleDeletionError,
    VehicleDoesNotExistsError,
    VehicleUpdateError,
)
from ..api.errors.database_errors import (
    DbRetrievalError,
    InvalidStatusError,
    InvalidFilterError,
)


class VehicleService(BaseService):
    """Service layer for handling core domain logic and workflows for Vehicles.

    Acts as an intermediary layer between the API endpoints and the underlying
    VehicleRepository, managing business rules, validations, and mapping data models
    to primitive dictionary structures.

    Attributes:
        vehicle_repo (VehicleRepository): Data repository abstraction layer for managing database persistence.
    """

    def __init__(self, db_conn: _connection) -> None:
        """Initializes the VehicleService with an active database connection.

        Args:
            db_conn (_connection): A live psycopg2 database connection.
        """
        self.vehicle_repo = VehicleRepository(db_conn)

    def register(
        self,
        make: str,
        model: str,
        model_year: int,
        vehicle_status: Optional[VehicleStatus],
    ) -> dict[str, Any]:
        """Registers a brand new vehicle within the inventory system.

        If a vehicle status is not explicitly provided, it defaults to AVAILABLE.

        Args:
            make (str): The manufacturer brand of the vehicle (e.g., 'Subaru').
            model (str): The specific model name of the vehicle (e.g., 'Outback').
            model_year (int): The calendar year the vehicle was manufactured.
            vehicle_status (Optional[VehicleStatus]): Initial status of the vehicle.

        Returns:
            dict[str, Any]: A dictionary representation of the newly created Vehicle entity.

        Raises:
            VehicleCreationError: If the repository fails to generate and return the
                newly registered vehicle entity from the database pipeline.
        """
        if vehicle_status is None:
            vehicle_status = VehicleStatus.AVAILABLE

        new_vehicle: Vehicle | None = self.vehicle_repo.create(
            make, model, model_year, vehicle_status
        )

        if new_vehicle is None:
            raise VehicleCreationError("unable to create Vehicle")

        return new_vehicle.to_dict()

    def get(self, id: int) -> dict[str, Any]:
        """Retrieves a single vehicle from the system by its unique database primary identifier.

        Args:
            id (int): The unique integer ID of the targeted vehicle record.

        Returns:
            dict[str, Any]: A dictionary representation of the requested Vehicle record.

        Raises:
            VehicleDoesNotExistsError: If no vehicle record matches the provided identifier.
            DbRetrievalError: On any unforeseen operational or network failures occurring
                within the database infrastructure layer.
        """
        try:
            vehicle = self.vehicle_repo.get_by_id(id)
            if vehicle is None:
                raise VehicleDoesNotExistsError(
                    f"vehicle with id: {id} does not exist in database"
                )
            return vehicle.to_dict()
        except psycopg2.Error as e:
            print(f"get vehicle error: {e}")
            raise DbRetrievalError("unable to retrieve Vehicle ")

    def get_all(self, status: dict[str, str] | None) -> list[dict[str, Any]]:
        """Queries and fetches collections of vehicle records applying dynamic field criteria filters.

        Args:
            status (dict[str, str] | None): Dictionary mapping filter attributes
                (like column keys and query text values) extracted from requested parameters.

        Returns:
            list[dict[str, Any]]: A list containing dictionary instances representing every
                matching vehicle found in the active scope. Returns an empty list if no matches exist.

        Raises:
            VehicleDoesNotExistsError: If the evaluation array length indicates an empty database collection.
            InvalidFilterError: If filter parameter validation logic triggers a baseline value error rejection.
            DbRetrievalError: If internal psycopg2 infrastructure exceptions interrupt structural parsing loops.
        """
        try:
            vehicles = self.vehicle_repo.get_all(status)
            if len(vehicles) < 1:
                return []

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

    def delete(self, id: int) -> dict[str, Any]:
        """Removes a vehicle record entirely out of active inventory operations.

        Args:
            id (int): The unique integer ID of the targeted vehicle record to be dropped.

        Returns:
            dict[str, Any]: A structural tracking dictionary holding metadata properties
                of the safely removed vehicle item.

        Raises:
            VehicleDoesNotExistsError: If a lookup operation returns empty because the target
                identifier row doesn't exist.
            VehicleDeletionError: If operational constraints fail (such as foreign key blocks
                triggered by active customer rental associations on this vehicle profile).
            DbRetrievalError: On unexpected hardware/connection drops occurring inside the system core.
        """
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

    def update_status(self, id: int, new_status: VehicleStatus) -> dict[str, Any]:
        """Transitions a vehicle's execution operational state configuration context.

        Args:
            id (int): The unique database reference tracking identifier for the vehicle.
            new_status (VehicleStatus): The target programmatic enumeration variable
                (e.g., VehicleStatus.RESERVED, VehicleStatus.AVAILABLE) to assign.

        Returns:
            dict[str, Any]: A serialized dictionary reflecting the updated vehicle data model attributes.

        Raises:
            InvalidStatusError: If parsed text elements fail internal verification checks
                mapping to a legitimate core enum item.
            VehicleDoesNotExistsError: If a verification query returns empty for the targeted row.
            VehicleUpdateError: If execution state records return a missing assignment indicator
                following statement processing attempts.
        """
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
