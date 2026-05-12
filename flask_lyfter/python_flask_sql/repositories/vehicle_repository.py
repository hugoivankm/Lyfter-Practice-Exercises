from typing import Optional

from psycopg2.extensions import connection as _connection
from ..models.vehicle import Vehicle, VehicleStatus
from .repository import BaseRepository


class VehicleRepository(BaseRepository):
    def __init__(self, db_conn: _connection) -> None:
        self.db = db_conn

    def create(
        self,
        make: str,
        model: str,
        model_year: int,
        vehicle_status: Optional[VehicleStatus],
    ):
        if vehicle_status not in VehicleStatus:
            vehicle_status = VehicleStatus.AVAILABLE

        with self.db.cursor() as cur:
            query = """
            INSERT INTO lyfter_car_rental.vehicles (make, model, model_year, vehicle_status)
            VALUES (%s, %s, %s, %s)
            RETURNING *
            """

            cur.execute(query, (make, model, model_year, vehicle_status))

            row = cur.fetchone()
            return Vehicle.from_row(row)

    def delete(self, vehicle_id: int) -> Optional[Vehicle]:
        with self.db.cursor() as cur:
            query: str = """
            DELETE FROM lyfter_car_rental.vehicles
            WHERE id = %s
            RETURNING *
            """

            cur.execute(query, (vehicle_id,))
            row = cur.fetchone()
            return Vehicle.from_row(row)

    def update_status(self, vehicle_id: int, status: VehicleStatus) -> Optional[Vehicle]:
        with self.db.cursor() as cur:
            if status not in VehicleStatus:
                return None
            query: str = """
            UPDATE lyfter_car_rental.vehicles
            SET vehicle_status = %s
            WHERE id = %s
            RETURNING *
            """

            cur.execute(query, (status, vehicle_id))
            row = cur.fetchone()
            return Vehicle.from_row(row)

    def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        query = """
            SELECT id, make, model, model_year, vehicle_status
            FROM lyfter_car_rental.vehicles 
            WHERE id = %s
        """
        with self.db.cursor() as cur:
            cur.execute(query, (vehicle_id,))
            row = cur.fetchone()
            return Vehicle.from_row(row)
