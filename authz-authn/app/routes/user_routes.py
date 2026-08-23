from typing import Any, cast
from flask import Blueprint, request, Response, jsonify, g, current_app
from app.services import UserService
from app.utils.decorators import login_required, admin_required, refresh_token_required
from app.utils.jwt_utils import JWTManager

user_bp = Blueprint("users", __name__)


@user_bp.route("/register", methods=["POST"])
@admin_required
def register():
    data = cast(dict[str, Any], request.get_json(silent=True) or {})
    username, password = data.get("username"), data.get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"error": "Username and password required"}), 400

    jwt = current_app.extensions["jwt_manager"]
    user_service = UserService(g.db_session, jwt)

    try:
        tokens = user_service.register(username, password)
        return jsonify(tokens), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


@user_bp.route("/login", methods=["POST"])
def login():
    raw_data = request.get_json(silent=True)
    if not isinstance(raw_data, dict):
        return (
            jsonify(
                {
                    "error": "Invalid or missing JSON payload. Please ensure Content-Type is application/json.",
                }
            ),
            400,
        )

    data = cast(dict[str, Any], raw_data)
    username = data.get("username")
    password = data.get("password")

    if "username" not in data or "password" not in data:
        return (
            jsonify(
                {
                    "error": "Missing required fields",
                }
            ),
            400,
        )

    if not isinstance(username, str) or not isinstance(password, str):
        return (
            jsonify({"error": "Invalid Data Type"}),
            400,
        )

    if not username.strip() or not password:
        return (
            jsonify(
                {
                    "error": "One or more empty values",
                }
            ),
            400,
        )
    jwt = cast(JWTManager | None, current_app.extensions.get("jwt_manager"))
    if not jwt:
        print("JWT Manager extension is not registered on current_app.")
        return (
            jsonify(
                {
                    "error": "Something went wrong",
                }
            ),
            500,
        )

    user_service = UserService(g.db_session, jwt)
    tokens = user_service.login(username.strip(), password)

    

    if not tokens:
        return (
            jsonify(
                {
                    "error": "Invalid username or password",
                }
            ),
            401,
        )

    return jsonify(tokens), 200


@user_bp.route("/me", methods=["GET"])
@login_required
def me():
    jwt = current_app.extensions["jwt_manager"]
    user_service = UserService(g.db_session, jwt)

    user = user_service.get_by_id(g.current_user_id)

    if not user:
        return Response(status=401)

    return jsonify(user.to_dict())


@user_bp.route("/refresh", methods=["POST"])
@refresh_token_required
def refresh():
    jwt_manager = current_app.extensions["jwt_manager"]

    token_data = jwt_manager.encode_access_token(
        {
            "sub": g.current_user_id,
            "role": g.current_user_role,
        }
    )

    return jsonify(token_data), 200
