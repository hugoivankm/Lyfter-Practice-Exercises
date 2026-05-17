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
        
    def get_by_id(self, id : int) -> Optional[Rental]:
        query = """
            SELECT id, users_id, vehicles_id, rental_date, status
            FROM lyfter_car_rental.rentals
            WHERE id = %s
        """

        with self.db.cursor() as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()
            return Rental.from_row(row)
    
    def update_status(self, id: int, status: RentalStatus) -> Optional[Rental]:
        with self.db.cursor() as cur:
            if status not in RentalStatus:
                return None
            query: str = """
            UPDATE lyfter_car_rental.rental
            SET rental_status = %s
            WHERE id = %s
            RETURNING *
            """
            
            cur.execute(query, (status, id))
            row = cur.fetchone()
            return Rental.from_row(row)
