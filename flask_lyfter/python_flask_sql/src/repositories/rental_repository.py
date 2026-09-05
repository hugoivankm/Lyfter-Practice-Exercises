from dataclasses import fields

from psycopg2 import sql
from psycopg2.extensions import connection as _connection
from psycopg2.sql import Composable

from ..models.rental import Rental, RentalStatus
from .repository import BaseRepository


class RentalRepository(BaseRepository):
    def __init__(self, db_conn: _connection) -> None:
        self.db = db_conn

    def create(
        self, users_id: int, vehicles_id: int, rental_status: RentalStatus
    ) -> Rental | None:
        with self.db.cursor() as cur:
            cur.execute(
                "INSERT INTO lyfter_car_rental.rentals (users_id, vehicles_id, rental_status) VALUES (%s, %s, %s) RETURNING *",
                (users_id, vehicles_id, rental_status),
            )

            row = cur.fetchone()
            return Rental.from_row(row)

    def get_by_id(self, id: int) -> Rental | None:
        query = """
            SELECT id, users_id, vehicles_id, rental_date, rental_status
            FROM lyfter_car_rental.rentals
            WHERE id = %s
        """

        with self.db.cursor() as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()
            return Rental.from_row(row)

    def update_status(self, id: int, status: RentalStatus) -> Rental | None:
        with self.db.cursor() as cur:
            if status not in RentalStatus:
                return None
            query: str = """
            UPDATE lyfter_car_rental.rentals
            SET rental_status = %s
            WHERE id = %s
            RETURNING *
            """

            cur.execute(query, (status, id))
            row = cur.fetchone()

            return Rental.from_row(row)

    def get_all(self, filters: dict[str, str] | None = None) -> list[Rental | None]:
        all_fields = fields(Rental)
        string_keys = {f.name for f in all_fields if f.type is str}

        allowed_keys = {f.name for f in all_fields}
        forbidden_key = {"id"}

        valid_keys = allowed_keys - forbidden_key

        base_query = """
            SELECT id, users_id, vehicles_id, rental_date, rental_status
            FROM lyfter_car_rental.rentals
        """

        query_parts: list[Composable] = [sql.SQL(base_query)]
        params: list[str] = []

        if filters:
            where_clauses: list[Composable] = []
            for key, value in filters.items():
                if key not in valid_keys:
                    raise ValueError(f"Invalid filter parameter: '{key}'")

                if key in string_keys:
                    where_clauses.append(
                        sql.SQL("{} ILIKE %s").format(sql.Identifier(key))
                    )
                else:
                    where_clauses.append(sql.SQL("{} = %s").format(sql.Identifier(key)))

                params.append(value)

            if where_clauses:
                query_parts.append(sql.SQL(" WHERE "))
                query_parts.append(sql.SQL(" AND ").join(where_clauses))

        final_query = sql.Composed(query_parts)

        with self.db.cursor() as cur:
            cur.execute(final_query, params)
            rows = cur.fetchall()
            return [Rental.from_row(row) for row in rows]
