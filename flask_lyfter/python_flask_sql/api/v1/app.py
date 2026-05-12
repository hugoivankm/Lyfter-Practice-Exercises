from flask import Flask, g, Response
from http import HTTPStatus
from psycopg2.extensions import connection as _connection
from psycopg2.extensions import TRANSACTION_STATUS_IDLE
from typing import Optional

from python_flask_sql.api.v1.responses import error_response
from ...database.database_manager import DbManager

from . import v1_bp

app = Flask(__name__)
app.register_blueprint(v1_bp, url_prefix="/api/v1")
db_manager = DbManager("postgres")


@app.before_request
def before_request():
    try:
        g.db = db_manager.get_connection()
        return None
    except Exception as e:
        print(f"Database Connection Error: {e}")
        return error_response("Something went wrong", HTTPStatus.SERVICE_UNAVAILABLE)


@app.after_request
def after_request(response: Response):
    db_conn: Optional[_connection] = getattr(g, "db", None)

    if db_conn is not None and 200 <= response.status_code < 300:
        try:
            db_conn.commit()
        except Exception as e:
            print(f"Database commit failed: {e}")
            db_conn.rollback()
            return error_response(
                "Something went wrong", HTTPStatus.INTERNAL_SERVER_ERROR
            )

    return response


@app.teardown_request
def teardown_request(exception: Optional[BaseException] = None) -> None:
    db_conn: Optional[_connection] = getattr(g, "db", None)

    if db_conn is not None:
        try:
            if db_conn.get_transaction_status() != TRANSACTION_STATUS_IDLE:
                db_conn.rollback()
        finally:
            db_manager.release_connection(db_conn)
        