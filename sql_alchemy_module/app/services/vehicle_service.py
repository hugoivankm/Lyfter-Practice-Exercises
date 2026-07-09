from typing import Any, Optional
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
        self, model: str, make: str, year: int, user_id: Optional[int], vin: str
    ) -> dict[str, Any]:

        new_vehicle = Vehicle(
            model=model, make=make, year=year, user_id=user_id, vin=vin
        )

        self.vehicles_repo.create(new_vehicle)

        self.vehicles_repo.session.flush()

        return {
            "id": new_vehicle.id,
            "model": new_vehicle.model,
            "make": new_vehicle.make,
            "year" : new_vehicle.year,
            "vin": new_vehicle.vin,
            "user_id": new_vehicle.user_id
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

    def get_all_vehicles(self, filter: Optional[str]) -> list[dict[str, Any]]:
        if filter == "no_user":
            vehicles =  self.vehicles_repo.get_by_no_user()
        else:
            stmt = select(Vehicle)
            vehicles = self.vehicles_repo.session.scalars(stmt).all()

        return [vehicle.to_dict() for vehicle in vehicles]

    def update_vehicle(self, vehicle_id: int, data: dict[str, Any]) -> dict[str, Any]:
        vehicle = self.vehicles_repo.get_by_id(vehicle_id)

        if vehicle is None:
            raise VehicleNotFoundError(
                f"vehicles with ID {vehicle_id} does not exist."
            )

        vehicle.model = str(data.get("model", vehicle.model))
        vehicle.make = str(data.get("make", vehicle.make))
        vehicle.year = int(data.get("year", vehicle.year))
        if data.get("user_id", vehicle.user_id): 
            vehicle.user_id = int(data.get("user_id", vehicle.user_id))

        self.vehicles_repo.save(vehicle)
        return vehicle.to_dict()
    

