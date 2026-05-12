from typing import Any
from psycopg2.extensions import connection as _connection


class RentalsRepository:
    def __init__(self, db_conn: _connection) -> None:
        self.db = db_conn

    def create(self, users_id: int, vehicles_id: int) -> (tuple[Any, ...] | None):
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO lyfter_car_rental.rentals (users_id, vehicles_id) VALUES (%s, %s) RETURNING id",
                (users_id, vehicles_id),
            )

            result: tuple[Any, ...] | None = cur.fetchone()
            
            if result:
                (rental_id,) = result
                return rental_id
            return None
