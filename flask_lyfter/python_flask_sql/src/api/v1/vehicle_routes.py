from http import HTTPStatus

import psycopg2
from flask import Blueprint, g, request

from ...services.vehicle_service import VehicleService
from ..errors.database_errors import DbRetrievalError, InvalidFilterError
from ..errors.json_errors import (
    EmptyJSONError,
    MalformedJSONError,
    MissingParametersJSONError,
)
from ..errors.vehicle_errors import VehicleDoesNotExistsError
from .responses import error_response, json_response
from .utils import update_status_and_respond, validate_json

vehicle_bp = Blueprint("vehicle_bp", __name__)


# POST api/v1/vehicles/
@vehicle_bp.route("/", methods=["POST"])
def create_vehicle():
    try:
        data = validate_json(request, ["make", "model", "model_year"])

        # Call service to handle creation
        service = VehicleService(g.db)
        vehicle_dict = service.register(
            data["make"], data["model"], data["model_year"], data.get("vehicle_status")
        )

        return json_response(vehicle_dict, HTTPStatus.CREATED)
    except MalformedJSONError:
        return error_response("Malformed JSON body", HTTPStatus.BAD_REQUEST)
    except EmptyJSONError:
        return error_response("Missing JSON body", HTTPStatus.BAD_REQUEST)
    except MissingParametersJSONError as e:
        return error_response(str(e), HTTPStatus.BAD_REQUEST)
    except Exception as e:
        print(e)
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
        )


# GET api/v1/vehicles
@vehicle_bp.route("/", methods=["GET"])
def list_vehicles():
    try:
        filters: dict[str, str] | None = request.args.to_dict()

        for key, value in filters.items():
            if value.strip() == "":
                return error_response(
                    f"Query parameter '{key}' cannot be empty", HTTPStatus.BAD_REQUEST
                )

        service = VehicleService(g.db)
        vehicles = service.get_all(filters)
        return json_response(vehicles)
    except VehicleDoesNotExistsError as ve:
        return error_response(str(ve), HTTPStatus.NOT_FOUND)
    except InvalidFilterError as fe:
        return error_response(str(fe), HTTPStatus.BAD_REQUEST)
    except DbRetrievalError as e:
        print(str(e))
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        print(str(e))
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
        )


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
    except Exception:
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
        )


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
    except Exception as e:
        print(str(e))
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
        )


# Special case checking the implementation of an action based endpoint
# in contrast with a resource based one
# PATCH api/v1/vehicles/<id>
@vehicle_bp.route("/<int:vehicle_id>", methods=["POST"])
def disable_vehicle(vehicle_id: int):
    try:
        data = validate_json(request, ["action"])

        action = data.get("action")
        if action == "disable":
            return update_status_and_respond(
                id=vehicle_id, service=VehicleService(g.db), new_status="unavailable"
            )
        return error_response("Invalid Action", HTTPStatus.BAD_REQUEST)

    except (MalformedJSONError, EmptyJSONError, MissingParametersJSONError) as e:
        return error_response(str(e), HTTPStatus.BAD_REQUEST)
    except Exception as e:
        print(str(e))
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
        )


# DELETE api/v1/vehicles/<id>
@vehicle_bp.route("/<int:vehicle_id>", methods=["DELETE"])
def delete_vehicle(vehicle_id: int):
    service = VehicleService(g.db)
    try:
        deleted_vehicle = service.delete(vehicle_id)
        return json_response(deleted_vehicle, HTTPStatus.OK)
    except psycopg2.IntegrityError:
        return error_response(
            "conflict with other records while deleting vehicle", HTTPStatus.CONFLICT
        )
    except VehicleDoesNotExistsError:
        return error_response("vehicle does not exist", HTTPStatus.UNPROCESSABLE_ENTITY)
    except Exception as e:
        print(str(e))
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
        )
