from flask import Blueprint, jsonify, g, request
from typing import Any, cast
from app.services.vehicle_service import VehicleService
from app.services.vehicle_service import VehicleNotFoundError


vehicle_bp = Blueprint("vehicles", __name__)

@vehicle_bp.route("/", methods=["GET"])
def get_vehicles():
    vehicle_service = VehicleService(g.db_session)

    filter = request.args.get("filter")
    if filter:
        filter = filter.lower()

    all_vehicles = vehicle_service.get_all_vehicles(filter)

    return jsonify(all_vehicles), 200


@vehicle_bp.route("/<int:id>", methods=["GET"])
def get_vehicle(id: int):
    vehicle_service = VehicleService(g.db_session)
    try:
        vehicle_data = vehicle_service.get_vehicle_by_id(id)
        return jsonify(vehicle_data), 200

    except VehicleNotFoundError:
        return jsonify({"error": f"Vehicle with ID {id} not found"}), 404


@vehicle_bp.route("/", methods=["POST"])
def register_vehicle():
    vehicle_service = VehicleService(g.db_session)
    required_keys = ["make", "model", "year", "vin"]

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
                {"error": f"Missing fields in vehicle: {', '.join(missing_params)}"}
            ), 401

        user_id = payload.get("user_id", None)
        if user_id:
            user_id = int(user_id)

        new_vehicle_dict = vehicle_service.register_new_vehicle(
            model=str(payload["model"]),
            make=str(payload["make"]),
            year=int(payload["year"]),
            vin=str(payload["vin"]),
            user_id=user_id,
        )
        
        return jsonify(new_vehicle_dict), 200
    except Exception as e:
        print(f"error: {e}")
        return jsonify({"error": "something went wrong"}), 500


@vehicle_bp.route("/<int:id>", methods=["DELETE"])
def delete_vehicle(id: int):
    vehicle_service = VehicleService(g.db_session)
    try:
        delete_vehicle_data = vehicle_service.delete_vehicle_by_id(id)
        return jsonify(delete_vehicle_data), 200
    except VehicleNotFoundError:
        return jsonify({"error": "vehicle not found"}), 404


@vehicle_bp.route("/<int:id>", methods=["PUT"])
def updated_vehicle(id: int):
    vehicle_service = VehicleService(g.db_session)
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        raw_data = request.get_json()
        if not isinstance(raw_data, dict):
            return jsonify({"error": "Invalid JSON format"}), 400

        payload = cast(dict[str, Any], raw_data)

        updated_vehicle = vehicle_service.update_vehicle(vehicle_id=id, data=payload)

        return jsonify(updated_vehicle), 200
    except VehicleNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as ex:
        print(ex)
        return jsonify({"error": "something went wrong"}), 500
