from typing import Any, cast

from app.services import UserNotFoundError, UserService
from flask import Blueprint, g, jsonify, request

user_bp = Blueprint("users", __name__)


@user_bp.route("/", methods=["GET"])
def get_users():
    user_service = UserService(g.db_session)
    filter = request.args.get("filter")
    if filter:
        filter = filter.lower()

    all_users = user_service.get_all_users(filter)

    return jsonify(all_users), 200


@user_bp.route("/<int:id>", methods=["GET"])
def get_user(id: int):
    user_service = UserService(g.db_session)
    try:
        view_param = request.args.get("view", "compact").lower()
        user_data = user_service.get_user_by_id(id, view_param)
        return jsonify(user_data), 200

    except UserNotFoundError:
        return jsonify({"error": f"User with ID {id} not found"}), 404


@user_bp.route("/", methods=["POST"])
def register_user():
    user_service = UserService(g.db_session)
    required_keys = ["full_name", "email", "phone_number"]

    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        raw_data = request.get_json()

        if not isinstance(raw_data, dict):
            return jsonify(
                {"error": "Invalid JSON format, expected a dictionary object"}
            ), 400

        payload = cast(dict[str, Any], raw_data)
        missing_params: list[str] = [
            field for field in required_keys if field not in payload
        ]

        if missing_params:
            return jsonify(
                {"error": f"Missing fields in user: {', '.join(missing_params)}"}
            ), 401

        new_user_dict = user_service.register_new_user(
            full_name=str(payload["full_name"]),
            email=str(payload["email"]),
            phone_number=str(payload["phone_number"]),
        )

        return jsonify(new_user_dict), 200
    except Exception as e:
        print(f"error: {e}")
        return jsonify({"error": "something went wrong"}), 500


@user_bp.route("/<int:id>", methods=["DELETE"])
def delete_user(id: int):
    user_service = UserService(g.db_session)
    try:
        delete_user_data = user_service.delete_user_by_id(id)
        return jsonify(delete_user_data), 200
    except UserNotFoundError:
        return jsonify({"error": "user not found"}), 404


@user_bp.route("/<int:id>", methods=["PUT"])
def update_user(id: int):
    user_service = UserService(g.db_session)
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        raw_data = request.get_json()
        if not isinstance(raw_data, dict):
            return jsonify({"error": "Invalid JSON format"}), 400

        payload = cast(dict[str, Any], raw_data)

        update_user = user_service.update_user(user_id=id, data=payload)

        return jsonify(update_user), 200
    except UserNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "something went wrong"}), 500
