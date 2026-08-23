import psycopg2
from psycopg2 import pool
from psycopg2.extensions import connection as _connection
from typing import Optional


class DbManager:
    def __init__(self, db_name: str) -> None:
        try:
            self._pool: pool.ThreadedConnectionPool = pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=20,
                host="localhost",
                port=5432,
                user="postgres",
                password="postgres",
                dbname=db_name,
            )
        except psycopg2.Error as e:
            print(f"database connection error: {e}")
            raise

    def get_connection(self) -> _connection:
        if not self._pool:
            raise Exception("Database pool not initialized")
        return self._pool.getconn()  # type: ignore[return-value]

    def release_connection(self, db_conn: Optional[_connection]) -> bool:
        if not self._pool or db_conn is None:
            return False

        try:
            self._pool.putconn(db_conn)  # type: ignore[reportUnknownMemberType]
            return True
        except Exception as e:
            print(f"failed to close cursor: {e}")
            return False
