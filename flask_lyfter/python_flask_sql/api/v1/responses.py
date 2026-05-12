from flask import jsonify
from typing import Any
from http import HTTPStatus

def json_response(data: dict[str, Any],  status_code: HTTPStatus = HTTPStatus.OK):
    return jsonify({
        "status": "success",
        "data" : data,
        "error": None,
    }), status_code.value

def error_response(message: str, status_code: HTTPStatus):
    return jsonify({
        "status": "error",
        "data": None,
        "error": {
            "message": message
        }
    }), status_code.value