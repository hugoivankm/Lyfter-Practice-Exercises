from flask import Blueprint, request, Response, jsonify
from app.services.user_service import UserService

def create_user_routes(service: UserService) -> Blueprint:
    user_bp = Blueprint("user", __name__)

    @user_bp.route("/register", methods=["POST"])
    def register(): # type: ignore[reportUnusedFunction]
        data = request.get_json()
        if not data or not data.get("username") or not data.get("password"):
            return Response(status=400)
        token = service.register(data["username"], data["password"])
        return jsonify(token=token)

    @user_bp.route("/login", methods=["POST"])
    def login(): # type: ignore[reportUnusedFunction]
        data = request.get_json()
        if not data or not data.get("username") or not data.get("password"):
            return Response(status=400)
        token = service.login(data["username"], data["password"])
        if not token:
            return Response(status=403)
        return jsonify(token=token)

    @user_bp.route("/me")
    def me(): # type: ignore[reportUnusedFunction]
        token = request.headers.get("Authorization")
        if not token:
            return Response(status=403)
        token = token.replace("Bearer ", "")
        user = service.get_user_from_token(token)
        if not user:
            return Response(status=403)
        return jsonify(user.to_dict())

    return user_bp
