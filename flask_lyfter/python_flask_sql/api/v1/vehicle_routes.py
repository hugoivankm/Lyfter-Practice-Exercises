import psycopg2
from http import HTTPStatus
from flask import Blueprint, g, request

from .utils import validate_json
from ...services.vehicle_service import (
    VehicleService,
    VehicleDoesNotExistsError,
    DbRetrievalError,
    VehicleUpdateError,
)

from ..errors.json_errors import (
    MalformedJSONError,
    EmptyJSONError,
    MissingParametersJSONError,
)

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

        new_status = data["vehicle_status"]

        service = VehicleService(g.db)
        service.update_status(vehicle_id, new_status)

        return json_response(new_status, HTTPStatus.OK)
    
    except MalformedJSONError:
        return error_response("Malformed JSON body", HTTPStatus.BAD_REQUEST)
    except EmptyJSONError:
        return error_response("Missing JSON body", HTTPStatus.BAD_REQUEST)
    except MissingParametersJSONError as e:
        return error_response(str(e), HTTPStatus.BAD_REQUEST)
    except VehicleDoesNotExistsError as e:
        return error_response(str(e), HTTPStatus.UNPROCESSABLE_ENTITY)
    except VehicleUpdateError as e:
        return error_response(str(e), HTTPStatus.NOT_FOUND)
    except psycopg2.errors.CheckViolation:
        return error_response("Invalid vehicle status", HTTPStatus.BAD_REQUEST)
    except Exception:
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
        )


# PATCH api/v1/vehicles/<id>
@vehicle_bp.route("/<int:vehicle_id>", methods=["PATCH"])
def disable_vehicle(vehicle_id: int):
    service = VehicleService(g.db)
    data = None

    try:
        data = request.get_json()
    except Exception:
        return error_response("Malformed JSON body", HTTPStatus.BAD_REQUEST)

    if not data:
        return error_response("Missing JSON body", HTTPStatus.BAD_REQUEST)

    required_fields = ["vehicle_status"]
    missing_params: list[str] = [
        field for field in required_fields if field not in data
    ]

    if missing_params:
        return error_response(
            f"{', '.join(missing_params)} missing from JSON body",
            HTTPStatus.BAD_REQUEST,
        )

    try:
        status = service.update_status(vehicle_id, "unavailable")
        return json_response(status, HTTPStatus.OK)
    except VehicleDoesNotExistsError as e:
        return error_response(str(e), HTTPStatus.UNPROCESSABLE_ENTITY)
    except VehicleUpdateError as e:
        return error_response(str(e), HTTPStatus.NOT_FOUND)
    except psycopg2.errors.CheckViolation:
        return error_response("Invalid vehicle status", HTTPStatus.BAD_REQUEST)
    except Exception:
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
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
