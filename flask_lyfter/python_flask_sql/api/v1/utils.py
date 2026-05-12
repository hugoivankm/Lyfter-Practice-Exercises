from flask import Request
from typing import Any, cast
from ...services.service import BaseService
from ..errors.json_errors import (
    MalformedJSONError,
    EmptyJSONError,
    MissingParametersJSONError,
)

from ...services.service import BaseService 


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


def _update_status_and_respond(id: int, new_status: str, service: BaseService):
    try:
        updated_metho
        return