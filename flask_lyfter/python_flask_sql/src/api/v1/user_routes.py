from flask import Blueprint, g, request
import psycopg2
from http import HTTPStatus

from .utils import validate_json, update_status_and_respond

from ...services.user_service import (
    UserService,
    UserDoesNotExistsError,
    DbRetrievalError,
    AlreadyExistsError,
    UserCreationError,
)

from ..errors.database_errors import InvalidFilterError

from ..errors.json_errors import (
    EmptyJSONError,
    MalformedJSONError,
    MissingParametersJSONError,
)
from .responses import json_response, error_response

user_bp = Blueprint("user_bp", __name__)


# POST api/v1/users/
@user_bp.route("/", methods=["POST"])
def create_user():
    try:
        # Parse JSON body
        try:
            data = request.get_json()
        except Exception:
            return error_response("Malformed JSON body", HTTPStatus.BAD_REQUEST)

        # Validate data
        if not data:
            return error_response("Missing JSON body", HTTPStatus.BAD_REQUEST)

        required_fields = ["email", "username", "password", "birthdate"]
        missing_params: list[str] = [
            field for field in required_fields if field not in data
        ]

        if missing_params:
            return error_response(
                f"{', '.join(missing_params)} missing from JSON body",
                HTTPStatus.BAD_REQUEST,
            )

        # Call service to handle creation
        service = UserService(g.db)

        user_dict = None
        if data.get("account_status"):
            user_dict = service.register(
                data["email"],
                data["username"],
                data["password"],
                data["birthdate"],
                data["account_status"],
            )
        else:
            user_dict = service.register(
                data["email"], data["username"], data["password"], data["birthdate"]
            )

        return json_response(user_dict, HTTPStatus.CREATED)

    except AlreadyExistsError:
        return error_response(
            "user email or user name already exists", HTTPStatus.CONFLICT
        )
    except UserCreationError:
        return error_response(
            "user must be created with a valid account status", HTTPStatus.BAD_REQUEST
        )
    except Exception:
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
        )


# GET api/v1/users/
@user_bp.route("/", methods=["GET"])
def list_users():
    try:
        filters: dict[str, str] | None = request.args.to_dict()

        for key, value in filters.items():
            if value.strip() == "":
                return error_response(
                    f"Query parameter '{key}' cannot be empty", HTTPStatus.BAD_REQUEST
                )

        service = UserService(g.db)
        users = service.get_all(filters)
        return json_response(users)
    except UserDoesNotExistsError as ue:
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


# GET api/v1/users/<id>
@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    try:
        service = UserService(g.db)
        user = service.get(user_id)
        return json_response(user)
    except UserDoesNotExistsError as e:
        return error_response(str(e), HTTPStatus.NOT_FOUND)
    except DbRetrievalError as e:
        return error_response(str(e), HTTPStatus.INTERNAL_SERVER_ERROR)
    except Exception:
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
        )


# PATCH api/v1/users/<id>
@user_bp.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id: int):
    try:
        data = validate_json(request, ["account_status"])
        return update_status_and_respond(
            user_id, data["account_status"], UserService(g.db)
        )
    except (MalformedJSONError, EmptyJSONError, MissingParametersJSONError) as e:
        return error_response(str(e), HTTPStatus.BAD_REQUEST)


# DELETE api/v1/users/<id>
@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    service = UserService(g.db)
    try:
        deleted_user = service.delete(user_id)
        return json_response(deleted_user, HTTPStatus.NO_CONTENT)
    except psycopg2.IntegrityError:
        return error_response(
            "conflict with other records while deleting user", HTTPStatus.CONFLICT
        )
    except UserDoesNotExistsError as e:
        return error_response(str(e), HTTPStatus.UNPROCESSABLE_ENTITY)
    except Exception:
        return error_response(
            "An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR
        )
