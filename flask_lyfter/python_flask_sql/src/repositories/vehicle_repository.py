from dataclasses import fields

from psycopg2 import sql
from psycopg2.extensions import connection as _connection
from psycopg2.sql import Composable

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
        vehicle_status: VehicleStatus | None,
    ) -> Vehicle | None:

        with self.db.cursor() as cur:
            query = """
            INSERT INTO lyfter_car_rental.vehicles (make, model, model_year, vehicle_status)
            VALUES (%s, %s, %s, %s)
            RETURNING *
            """

            cur.execute(query, (make, model, model_year, vehicle_status))

            row = cur.fetchone()
            return Vehicle.from_row(row)

    def delete(self, vehicle_id: int) -> Vehicle | None:
        with self.db.cursor() as cur:
            query: str = """
            DELETE FROM lyfter_car_rental.vehicles
            WHERE id = %s
            RETURNING *
            """

            cur.execute(query, (vehicle_id,))
            row = cur.fetchone()
            return Vehicle.from_row(row)

    def update_status(
        self, vehicle_id: int, status: VehicleStatus
    ) -> Vehicle | None:
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

    def get_by_id(self, vehicle_id: int) -> Vehicle | None:
        query = """
            SELECT id, make, model, model_year, vehicle_status
            FROM lyfter_car_rental.vehicles 
            WHERE id = %s
        """
        with self.db.cursor() as cur:
            cur.execute(query, (vehicle_id,))
            row = cur.fetchone()
            return Vehicle.from_row(row)

    def get_all(self, filters: dict[str, str] | None = None) -> list[Vehicle | None]:
        all_fields = fields(Vehicle)
        string_keys = {f.name for f in all_fields if f.type is str}

        allowed_keys = {f.name for f in all_fields}
        forbidden_key = {"id"}

        valid_keys = allowed_keys - forbidden_key

        base_query = """
            SELECT id, make, model, model_year, vehicle_status
            FROM lyfter_car_rental.vehicles 
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
            return [Vehicle.from_row(row) for row in rows]
