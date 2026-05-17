from datetime import date
from typing import Optional
from dataclasses import fields

from psycopg2.extensions import connection as _connection
from psycopg2 import sql
from psycopg2.sql import Composable

from .repository import BaseRepository
from ..models.user import User, AccountStatus



class UserRepository(BaseRepository):
    def __init__(self, db_conn: _connection):
        self.db = db_conn

    def create(
        self,
        email: str,
        username: str,
        password: str,
        birthdate: date,
        account_status: AccountStatus,
    ) -> User | None:
        with self.db.cursor() as cur:
            query: str = """
            INSERT INTO lyfter_car_rental.users (email, username, password, birthdate, account_status)
            VALUES (%s, %s, %s, %s, %s) 
            RETURNING *
            """

            cur.execute(
                query,
                (email, username, password, birthdate, account_status),
            )
            row = cur.fetchone()
            return User.from_row(row)

    def get_by_id(self, id: int) -> Optional[User]:
        self.db.rollback()

        query = """
            SELECT id, email, username, password, birthdate, account_status 
            FROM lyfter_car_rental.users 
            WHERE id = %s
        """

        with self.db.cursor() as cur:
            cur.execute(query, (id,))
            row = cur.fetchone()
            return User.from_row(row)

    def delete(self, id: int) -> User | None:
        with self.db.cursor() as cur:
            query: str = """
            DELETE FROM lyfter_car_rental.users
            WHERE id = %s
            RETURNING *
            """

            cur.execute(query, (id,))
            row = cur.fetchone()
            return User.from_row(row)

    def update_status(self, id: int, status: AccountStatus) -> User | None:
        with self.db.cursor() as cur:
            if status not in AccountStatus:
                return None
            query: str = """
            UPDATE lyfter_car_rental.users
            SET account_status = %s
            WHERE id = %s
            RETURNING *
            """
            cur.execute(query, (status.value, id))
            row = cur.fetchone()
            return User.from_row(row)
    
    def get_all(self, filters: dict[str, str] | None = None) -> list[Optional[User]]:
        allowed_keys = {f.name for f in fields(User)}

        base_query = """
            SELECT id, email, username, password, birthdate, account_status
            FROM lyfter_car_rental.users
        """

        query_parts: list[Composable] = [sql.SQL(base_query)]
        params: list[str] = []

        if filters:
            where_clauses: list[Composable] = []
            for key, value in filters.items():
                if key not in allowed_keys:
                    raise ValueError(f"Invalid filter parameter: '{key}'")

                where_clauses.append(sql.SQL("{} = %s").format(sql.Identifier(key)))

                params.append(value)

            if where_clauses:
                query_parts.append(sql.SQL(" WHERE "))
                query_parts.append(sql.SQL(" AND ").join(where_clauses))

        final_query = sql.Composed(query_parts)

        with self.db.cursor() as cur:
            cur.execute(final_query, params)
            rows = cur.fetchall()
            return [User.from_row(row) for row in rows]
