from typing import Optional
from psycopg2.extensions import connection as _connection

from .repository import BaseRepository
from ..models.rental import Rental, RentalStatus


class RentalRepository(BaseRepository):
    def __init__(self, db_conn: _connection) -> None:
        self.db = db_conn

    def create(
        self, users_id: int, vehicles_id: int, rental_status: RentalStatus
    ) -> Optional[Rental]:
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO lyfter_car_rental.rentals (users_id, vehicles_id, status) VALUES (%s, %s, %s) RETURNING *",
                (users_id, vehicles_id, rental_status),
            )

            row = cur.fetchone()
            return Rental.from_row(row)
