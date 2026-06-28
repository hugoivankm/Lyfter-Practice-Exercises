from flask import Flask, g
from app.routes import v1_bp
from .database.db_manager import DatabaseManager


app = Flask(__name__)
db_manager: DatabaseManager = DatabaseManager(
    "postgresql://postgres:postgres@localhost/postgres?options=-csearch_path=sql_alchemy_module"
)

app.register_blueprint(v1_bp, url_prefix='/api/v1')

@app.before_request
def create_db_session():
    g.db_session = db_manager.create_session()


@app.teardown_request
def teardown_db_session(exception: BaseException | None = None):
    session = getattr(g, "db_session", None)

    if session is not None:
        try:
            if exception is None:
                session.commit()
            else:
                session.rollback()
        except Exception:
            session.rollback()
        finally:
            session.close()
