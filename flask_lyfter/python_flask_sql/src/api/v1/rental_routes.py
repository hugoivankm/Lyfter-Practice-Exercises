from http import HTTPStatus

from flask import Blueprint, g, request

from ...services.rental_service import RentalService
from ..errors.database_errors import DbRetrievalError, InvalidFilterError
from ..errors.json_errors import (
    EmptyJSONError,
    MalformedJSONError,
    MissingParametersJSONError,
)
from ..errors.rental_errors import RentalCreationError, RentalDoesNotExistsError
from .responses import error_response, json_response
from .utils import update_status_and_respond, validate_json

rental_bp = Blueprint("rental_bp", __name__)


# POST api/v1/rentals/
@rental_bp.route("/", methods=["POST"])
def create_rental():
    # Parse inputs
    try:
        data = request.get_json()
    except Exception:
        return error_response("Malformed JSON body", HTTPStatus.BAD_REQUEST)

    # Validate data
    if not data:
        return error_response("Missing JSON body", HTTPStatus.BAD_REQUEST)

    required_fields = ["users_id", "vehicles_id"]
    missing_params: list[str] = [
        field for field in required_fields if field not in data
    ]

    if missing_params:
        return error_response(
            f"{', '.join(missing_params)} missing from JSON body",
            HTTPStatus.BAD_REQUEST,
        )

    # Call service to handle creation
    try:
        service = RentalService(g.db)

        rental_dict = None
        if data.get("rental_status"):
            rental_dict = service.register(
                data["users_id"],
                data["vehicles_id"],
                data["rental_status"],
            )
        else:
            rental_dict = service.register(
                data["users_id"],
                data["vehicles_id"],
            )

        return json_response(rental_dict, HTTPStatus.CREATED)

    except RentalCreationError as e:
        print(str(e))
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        print(str(e))
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
        )


# GET api/v1/rentals/
@rental_bp.route("/", methods=["GET"])
def list_rentals():
    try:
        filters: dict[str, str] | None = request.args.to_dict()

        for key, value in filters.items():
            if value.strip() == "":
                return error_response(
                    f"Query parameter '{key}' cannot be empty", HTTPStatus.BAD_REQUEST
                )

        service = RentalService(g.db)
        rentals = service.get_all(filters)
        return json_response(rentals)
    except RentalDoesNotExistsError as ue:
        return error_response(str(ue), HTTPStatus.NOT_FOUND)
    except InvalidFilterError as fe:
        return error_response(str(fe), HTTPStatus.BAD_REQUEST)
    except DbRetrievalError:
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        print(str(e))
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
        )


# GET api/v1/rentals/<id>
@rental_bp.route("/<int:rental_id>", methods=["GET"])
def get_rental(rental_id: int):
    service = RentalService(g.db)
    try:
        rental = service.get(rental_id)
        return json_response(rental, HTTPStatus.OK)
    except RentalDoesNotExistsError as e:
        return error_response(str(e), HTTPStatus.NOT_FOUND)
    except DbRetrievalError as e:
        return error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
    except Exception:
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
        )


# PATCH api/v1/rentals/<id>
@rental_bp.route("/<int:rental_id>", methods=["PATCH"])
def update_rental(rental_id: int):
    try:
        data = validate_json(request, ["rental_status"])

        return update_status_and_respond(
            rental_id, data["rental_status"], RentalService(g.db)
        )

    except (MalformedJSONError, EmptyJSONError, MissingParametersJSONError) as e:
        return error_response(str(e), HTTPStatus.BAD_REQUEST)


# Simulation of a forbidden endpoint, this project doesn't support authorization or authentication
# DELETE api/v1/rentals/<id>
@rental_bp.route("/<int:rental_id>", methods=["DELETE"])
def delete_rental(rental_id: int):
    print("forbidden request")
    return error_response("Forbidden", HTTPStatus.FORBIDDEN)
