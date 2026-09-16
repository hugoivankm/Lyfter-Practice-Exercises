from collections.abc import Callable
from functools import wraps
from typing import Any, cast

import jwt
from flask import current_app, g, jsonify, request


def login_required[F: Callable[..., Any]](f: F) -> F:
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any):
        auth_header: str | None = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"error": "Authorization header is missing"}), 401

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify(
                {"error": "Authorization header must be 'Bearer <token>'"}
            ), 401

        token = parts[1]
        try:
            jwt_manager = current_app.extensions.get("jwt_manager")
            if not jwt_manager:
                return jsonify({"error": "JWT is not configured"}), 500

            payload = jwt_manager.decode(token)
            if payload is None:
                return jsonify({"error": "Invalid or expired token"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        if payload.get("type") != "access":
            return jsonify({"error": "Access token required"}), 403

        g.current_user_id = int(payload["sub"])
        g.current_user_role = payload.get("role")

        return f(*args, **kwargs)

    return cast(F, wrapper)


def admin_required[F: Callable[..., Any]](f: F) -> F:
    @login_required
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any):
        if getattr(g, "current_user_role", None) != "admin":
            return jsonify({"error": "Forbidden: Admin privileges required"}), 403
        return f(*args, **kwargs)

    return cast(F, wrapper)


def refresh_token_required[F: Callable[..., Any]](f: F) -> F:
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any):
        auth_header: str | None = request.headers.get("Authorization")
        token: str | None = None

        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]

        if not token and request.is_json:
            body: Any = request.get_json(silent=True)
            if isinstance(body, dict):
                data = cast(dict[str, Any], body)
                raw_token = data.get("refresh_token")
                if isinstance(raw_token, str):
                    token = raw_token

        if not token:
            return jsonify({"error": "Refresh token is missing"}), 400

        jwt_manager = current_app.extensions.get("jwt_manager")
        if not jwt_manager:
            return jsonify({"error": "JWT is not configured"}), 500

        try:
            payload = jwt_manager.decode(token)
            if payload is None:
                return jsonify({"error": "Invalid or expired token"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify(
                {"error": "Refresh token expired. Please log in again."}
            ), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid refresh token"}), 401

        if payload.get("type") != "refresh":
            return jsonify({"error": "Token is not a refresh token"}), 400

        g.current_user_id = int(payload["sub"])
        g.current_user_role = payload.get("role")

        return f(*args, **kwargs)

    return cast(F, wrapper)
