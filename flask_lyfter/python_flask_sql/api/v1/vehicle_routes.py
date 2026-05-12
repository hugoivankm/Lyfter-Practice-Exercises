import psycopg2
from http import HTTPStatus
from flask import Blueprint, g, request

from .utils import validate_json, update_status_and_respond

from ...services.vehicle_service import VehicleService

from ..errors.json_errors import (
    MalformedJSONError,
    EmptyJSONError,
    MissingParametersJSONError,
)

from ..errors.vehicle_errors import VehicleDoesNotExistsError

from ..errors.database_errors import DbRetrievalError

from .responses import json_response, error_response

vehicle_bp = Blueprint("vehicle_bp", __name__)


# POST api/v1/vehicles/
@vehicle_bp.route("/", methods=["POST"])
def create_vehicle():
    try:
        data = validate_json(request, ["make", "model", "model_year"])
    except MalformedJSONError:
        return error_response("Malformed JSON body", HTTPStatus.BAD_REQUEST)
    except EmptyJSONError:
        return error_response("Missing JSON body", HTTPStatus.BAD_REQUEST)
    except MissingParametersJSONError as e:
        return error_response(str(e), HTTPStatus.BAD_REQUEST)

    # Call service to handle creation
    service = VehicleService(g.db)
    vehicle_dict = service.register(
        data["make"], data["model"], data["model_year"], data.get("vehicle_status")
    )

    return json_response(vehicle_dict, HTTPStatus.CREATED)


# GET api/v1/vehicles
@vehicle_bp.route("/", methods=["GET"])
def list_vehicles():
    raise NotImplementedError()


# GET api/v1/vehicles/<id>
@vehicle_bp.route("/<int:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id: int):
    service = VehicleService(g.db)
    try:
        vehicle = service.get(vehicle_id)
        return json_response(vehicle)
    except VehicleDoesNotExistsError as e:
        return error_response(str(e), HTTPStatus.NOT_FOUND)
    except DbRetrievalError as e:
        return error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)


# PATCH api/v1/vehicles/<id>
@vehicle_bp.route("/<int:vehicle_id>", methods=["PATCH"])
def update_vehicle_status(vehicle_id: int):
    try:
        data = validate_json(request, ["vehicle_status"])

        return update_status_and_respond(
            vehicle_id, data["vehicle_status"], VehicleService(g.db)
        )

    except (MalformedJSONError, EmptyJSONError, MissingParametersJSONError) as e:
        return error_response(str(e), HTTPStatus.BAD_REQUEST)


# PATCH api/v1/vehicles/<id>
@vehicle_bp.route("/<int:vehicle_id>/disable", methods=["POST"])
def disable_vehicle(vehicle_id: int):
    return update_status_and_respond(
        id=vehicle_id,
        service=VehicleService(g.db),
        new_status="unavailable"
    )

# DELETE api/v1/vehicles/<id>
@vehicle_bp.route("/<int:vehicle_id>", methods=["DELETE"])
def delete_vehicle(vehicle_id: int):
    service = VehicleService(g.db)
    try:
        deleted_vehicle = service.delete(vehicle_id)
        return json_response(deleted_vehicle, HTTPStatus.NO_CONTENT)
    except psycopg2.IntegrityError:
        return error_response(
            "conflict with other records while deleting vehicle", HTTPStatus.CONFLICT
        )
    except VehicleDoesNotExistsError:
        return error_response("vehicle does not exist", HTTPStatus.UNPROCESSABLE_ENTITY)
    except Exception:
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
        )
