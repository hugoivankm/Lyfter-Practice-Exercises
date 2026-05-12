from flask import Request
from typing import Any, cast, Protocol
from http import HTTPStatus
import psycopg2

from ..errors.json_errors import (
    MalformedJSONError,
    EmptyJSONError,
    MissingParametersJSONError,
)

from ..errors.vehicle_errors import VehicleDoesNotExistsError, VehicleUpdateError
from ..errors.user_errors import UserDoesNotExistsError, UserUpdateError
from .responses import json_response, error_response

class StatusUpdatable(Protocol):
    def update_status(self, id: int, new_status: Any) -> dict[str, Any]: ...


def validate_json(
    request: Request, required_keys: list[str]
) -> dict[str, Any]:
    try:
        data: Any = request.get_json()
    except Exception:
        raise MalformedJSONError("Malformed JSON body")

    if data is None or not isinstance(data, dict):
        raise EmptyJSONError("Missing or invalid JSON body")

    missing_params: list[str] = [field for field in required_keys if field not in data]

    if missing_params:
        raise MissingParametersJSONError(
            f"{', '.join(missing_params)} missing from JSON body"
        )

    return cast(dict[str, Any], data)


def update_status_and_respond(id: int, new_status: str, service: StatusUpdatable):
    try:
        result = service.update_status(id, new_status)
        return json_response(result, HTTPStatus.OK)
    
    # --- JSON Errors ---
    except (MalformedJSONError, EmptyJSONError) as e:
        return error_response(str(e), HTTPStatus.BAD_REQUEST)
    except MissingParametersJSONError as e:
        return error_response(str(e), HTTPStatus.BAD_REQUEST)
        
    # --- Vehicle Errors ---
    except VehicleDoesNotExistsError as e:
        return error_response(str(e), HTTPStatus.UNPROCESSABLE_ENTITY)
    except VehicleUpdateError as e:
        return error_response(str(e), HTTPStatus.NOT_FOUND)
    
    # --- Database Errors ---
    except psycopg2.errors.CheckViolation:
        return error_response("Invalid status", HTTPStatus.BAD_REQUEST)
    
    # --- User Errors ---     
    except UserDoesNotExistsError as e:
        return error_response(str(e), HTTPStatus.UNPROCESSABLE_ENTITY)
    except UserUpdateError as e:
        return error_response(str(e), HTTPStatus.NOT_FOUND)


    except Exception as e:
        print(f"Unexpected error: {e}")
        return error_response("An unexpected error occurred", HTTPStatus.INTERNAL_SERVER_ERROR)