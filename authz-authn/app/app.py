from flask import Flask, g
from flask.json.provider import DefaultJSONProvider
from app.database.db_manager import DatabaseManager
from app.utils.jwt_utils import JWT_Manager
from app.models.model import Base
from app.routes import user_bp, product_bp, invoice_bp


def create_app() -> Flask:
    app = Flask(__name__)

    db_manager = DatabaseManager(
        "postgresql://postgres:postgres@localhost/postgres?options=-csearch_path=authz-authn"
    )
    db_manager.create_tables(Base)

    jwt = JWT_Manager(secret="FWWGKXAM9Q61J8WS2SGAIXKMOKYS3QKV", algorithm="HS256")
    app.extensions["jwt_manager"] = jwt  

    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(product_bp, url_prefix="/products")
    app.register_blueprint(invoice_bp, url_prefix="/invoices")

    @app.route("/liveness")
    def liveness():
        return "<p>Hello, World!</p>"

    # preserve dict key order when marshalling/unmarshalling json
    class UnsortedJSONProvider(DefaultJSONProvider):
        sort_keys = False

    app.json = UnsortedJSONProvider(app)

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

    return app
