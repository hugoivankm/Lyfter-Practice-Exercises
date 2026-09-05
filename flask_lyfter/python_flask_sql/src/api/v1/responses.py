from http import HTTPStatus
from typing import Any

from flask import jsonify


def json_response(
    data: dict[str, Any] | list[dict[str, Any]], status_code: HTTPStatus = HTTPStatus.OK
):
    return jsonify(
        {
            "status": "success",
            "data": data,
            "error": None,
        }
    ), status_code.value


def error_response(message: str, status_code: HTTPStatus):
    return jsonify(
        {"status": "error", "data": None, "error": {"message": message}}
    ), status_code.value
