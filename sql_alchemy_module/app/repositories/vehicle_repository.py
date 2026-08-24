
from app.models import Vehicle
from sqlalchemy import select
from sqlalchemy.orm import Session


class VehicleRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        return self.session.get(Vehicle, vehicle_id)

    def create(self, vehicle: Vehicle) -> Vehicle:
        self.session.add(vehicle)
        return vehicle

    def delete(self, vehicle: Vehicle):
        self.session.delete(vehicle)

    def save(self, vehicle: Vehicle) -> Vehicle:
        self.session.add(vehicle)
        return vehicle

    def get_by_no_user(self) -> list[Vehicle]:
        stmt = select(Vehicle).where(Vehicle.user_id.is_(None))
        return list(self.session.scalars(stmt).all())
