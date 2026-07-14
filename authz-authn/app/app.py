from flask import Flask
from app.routes.user_routes import create_user_routes
from app.database.db_manager import DatabaseManager
from app.repositories.user_repository import UserRepository
from app.utils.jwt_utils import JWT_Manager
from app.services.user_service import UserService
from app.models.model import Base

def create_app() -> Flask:
    app = Flask("user-service")

    db = DatabaseManager(
    "postgresql://postgres:postgres@localhost/postgres?options=-csearch_path=authz-authn"
)
    db.create_tables(Base)

 
    repo = UserRepository(db)
    jwt = JWT_Manager(secret="trespatitos", algorithm="HS256")
    service = UserService(repo, jwt)


    app.register_blueprint(create_user_routes(service))

    @app.route("/liveness")
    def liveness(): # type: ignore[reportUnusedFunction]
        return "<p>Hello, World!</p>"

    return app