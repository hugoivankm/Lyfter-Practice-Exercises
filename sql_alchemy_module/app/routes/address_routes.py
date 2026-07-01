from flask import Blueprint, jsonify, g, request
from typing import Any, cast
from app.services.address_service import AddressService, AddressNotFoundError
from app.services.address_service import UserNotFoundError


address_bp = Blueprint("address", __name__)


@address_bp.route("/", methods=["GET"])
def get_addresss():
    address_service = AddressService(g.db_session)

    all_addresses = address_service.get_all_addresses()

    return jsonify(all_addresses), 200


@address_bp.route("/<int:id>", methods=["GET"])
def get_address(id: int):
    address_service = AddressService(g.db_session)
    try:
        address_data = address_service.get_address_by_id(id)
        return jsonify(address_data), 200

    except AddressNotFoundError:
        return jsonify({"error": f"Address with ID {id} not found"}), 404


@address_bp.route("/", methods=["POST"])
def register_address():
    address_service = AddressService(g.db_session)
    required_keys = ["physical_address", "user_id"]

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
                {"error": f"Missing fields in address: {', '.join(missing_params)}"}
            ), 401

        new_address_dict = address_service.register_new_address(
            physical_address=str(payload["physical_address"]), user_id=int(payload["user_id"])
        )

        return jsonify(new_address_dict), 200
    except UserNotFoundError as ue:
        print(f"error: {ue}")
        return jsonify({"error": "Unable to find user"})
    except Exception as e:
        print(f"error: {e}")
        return jsonify({"error": "something went wrong"})


@address_bp.route("/<int:id>", methods=["DELETE"])
def delete_address(id: int):
    address_service = AddressService(g.db_session)
    try:
        delete_address_data = address_service.delete_address_by_id(id)
        return jsonify(delete_address_data), 200
    except AddressNotFoundError:
        return jsonify({"error": "address not found"}, 404)


@address_bp.route("/<int:id>", methods=["PUT"])
def update_address(id: int):
    address_service = AddressService(g.db_session)
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        raw_data = request.get_json()
        if not isinstance(raw_data, dict):
            return jsonify({"error": "Invalid JSON format"}), 400

        payload = cast(dict[str, Any], raw_data)

        updated_address = address_service.update_address(address_id=id, data=payload)

        return jsonify(updated_address), 200
    except AddressNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception:
        return jsonify({"error": "something went wrong"}), 500
