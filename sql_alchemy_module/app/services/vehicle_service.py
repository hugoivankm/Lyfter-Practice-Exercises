from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.repositories.vehicle_repository import VehicleRepository
from app.models.vehicle import Vehicle


class VehicleNotFoundError(Exception):
    "Vehicle not found"

    pass


class VehicleService:
    def __init__(self, session: Session) -> None:
        self.vehicles_repo = VehicleRepository(session)

    def register_new_vehicle(
        self, model: str, make: str, year: int, vehicles_id: int, vin: str
    ) -> dict[str, Any]:

        new_vehicle = Vehicle(
            model=model, make=make, year=year, vehicles_id=vehicles_id, vin=vin
        )

        self.vehicles_repo.create(new_vehicle)

        self.vehicles_repo.session.flush()

        return {
            "id": new_vehicle.id,
        }

    def get_vehicle_by_id(self, id: int):
        vehicle = self.vehicles_repo.get_by_id(id)

        if vehicle is None:
            raise VehicleNotFoundError(f"Vehicle with id: {id} not found")

        return vehicle.to_dict()

    def delete_vehicle_by_id(self, id: int):
        vehicle = self.vehicles_repo.get_by_id(id)
        if vehicle is None:
            raise VehicleNotFoundError(f"Vehicle with id: {id} not found")

        vehicle_dict = vehicle.to_dict()

        self.vehicles_repo.delete(vehicle)

        return vehicle_dict

    def get_all_vehicles(self) -> list[dict[str, Any]]:
        stmt = select(Vehicle)

        vehicles = self.vehicles_repo.session.scalars(stmt).all()

        return [vehicle.to_dict() for vehicle in vehicles]

    def update_vehicles(self, vehicles_id: int, data: dict[str, Any]) -> dict[str, Any]:
        vehicles = self.vehicles_repo.get_by_id(vehicles_id)

        if vehicles is None:
            raise VehicleNotFoundError(
                f"vehicles with ID {vehicles_id} does not exist."
            )

        vehicles.model = str(data.get("model", vehicles.model))
        vehicles.make = str(data.get("make", vehicles.make))
        vehicles.year = int(data.get("year", vehicles.year))

        self.vehicles_repo.save(vehicles)
        return vehicles.to_dict()
