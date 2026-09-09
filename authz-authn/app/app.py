from typing import Any

from app.database.db_manager import DatabaseManager
from app.models import Base, Product, User
from app.routes import contact_bp, invoice_bp, order_bp, product_bp, user_bp
from app.utils.jwt_utils import JWTManager
from flask import Flask, g
from flask.json.provider import DefaultJSONProvider
from werkzeug.security import generate_password_hash


def seed_demo_admin(db_manager: DatabaseManager) -> None:
    session = db_manager.create_session()
    try:
        admin = session.query(User).filter_by(username="admin").first()
        if not admin:
            demo_admin = User(
                username="admin",
                password=generate_password_hash("admin"),
                role="admin",
            )
            session.add(demo_admin)
            session.commit()
            print("Initial admin user created")
        else:
            if not admin.password.startswith(("scrypt:", "pbkdf2:")):
                admin.password = generate_password_hash("admin")
                session.commit()
                print("Updated existing admin password to valid hash")
    except Exception as e:
        session.rollback()
        print(f"Failed to seed demo admin: {e}")
    finally:
        session.close()


def seed_demo_products(db_manager: DatabaseManager) -> None:
    session = db_manager.create_session()
    fruits: list[dict[str, Any]] = [
        {"name": "Apple", "price": 1.50, "quantity": 100},
        {"name": "Banana", "price": 0.75, "quantity": 150},
        {"name": "Orange", "price": 1.25, "quantity": 80},
        {"name": "Strawberry", "price": 3.99, "quantity": 50},
        {"name": "Watermelon", "price": 5.50, "quantity": 25},
    ]

    try:
        added_count = 0
        for fruit in fruits:
            existing = session.query(Product).filter_by(name=fruit["name"]).first()
            if not existing:
                product = Product(
                    name=fruit["name"],
                    price=fruit["price"],
                    quantity=fruit["quantity"],
                )
                session.add(product)
                added_count += 1

        if added_count > 0:
            session.commit()
            print("Successfully seeded products")
    except Exception as e:
        session.rollback()
        print(f"Failed to seed fruit products: {e}")
    finally:
        session.close()


def create_app() -> Flask:
    app = Flask(__name__)

    db_manager = DatabaseManager(
        "postgresql://postgres:postgres@localhost/postgres?options=-csearch_path=authz-authn"
    )

    db_manager.create_tables(Base)

    seed_demo_admin(db_manager)
    seed_demo_products(db_manager)

    jwt = JWTManager(algorithm="RS256")
    app.extensions["jwt_manager"] = jwt

    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(product_bp, url_prefix="/products")
    app.register_blueprint(invoice_bp, url_prefix="/invoices")
    app.register_blueprint(order_bp, url_prefix="/orders")
    app.register_blueprint(contact_bp, url_prefix="/contacts")

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
