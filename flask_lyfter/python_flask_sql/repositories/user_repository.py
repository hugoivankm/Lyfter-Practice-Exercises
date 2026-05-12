from psycopg2.extensions import connection as _connection
from datetime import date
from ..models.user import User, AccountStatus
from typing import Optional

from .repository import BaseRepository

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
