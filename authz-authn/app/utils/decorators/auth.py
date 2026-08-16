from functools import wraps
from flask import request, jsonify, g, current_app
from typing import Callable, Any, cast


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

        jwt_manager = current_app.extensions.get("jwt_manager")
        if not jwt_manager:
            return jsonify({"error": "JWT is not configured"}), 500

        payload = jwt_manager.decode(token)

        if payload is None:
            return jsonify({"error": "Invalid or expired token"}), 401
    
        g.current_user_id = payload.get("id")
        g.current_user_role = payload.get("role")


        return f(*args, **kwargs)

    return cast(F, wrapper)

def admin_required[F: Callable[..., Any]](f: F) -> F:
    @login_required
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any):
        if getattr(g, "current_user_role", None) != "admin":
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)

    return cast(F, wrapper)

