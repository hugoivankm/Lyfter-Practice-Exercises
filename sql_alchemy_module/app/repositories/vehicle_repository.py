from typing import Optional
from sqlalchemy.orm import Session
from app.models import Vehicle

class VehicleRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        return self.session.get(Vehicle, vehicle_id)

    def create(self, vehicle: Vehicle) -> Vehicle:
        self.session.add(vehicle)
        return vehicle

    def delete(self, vehicle: Vehicle):
        self.session.delete(vehicle)

    def save(self, vehicle: Vehicle) -> Vehicle:
        self.session.add(vehicle)
        return vehicle
