from flask import Blueprint, request, Response, jsonify, g, current_app
from app.services import UserService
from app.utils.decorators import login_required
from app.utils.decorators import admin_required

user_bp = Blueprint("users", __name__)

@user_bp.route("/register", methods=["POST"])
@admin_required
def register():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return Response(status=400)

    jwt = current_app.extensions["jwt_manager"]
    user_service = UserService(g.db_session, jwt)

    token = user_service.register(data["username"], data["password"])
    return jsonify(token=token)

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return Response(status=400)

    jwt = current_app.extensions["jwt_manager"]
    user_service = UserService(g.db_session, jwt)

    token = user_service.login(data["username"], data["password"])
    if not token:
        return Response(status=401)
    return jsonify(token=token)

@user_bp.route("/me", methods=["GET"]) 
@login_required
def me():
    jwt = current_app.extensions["jwt_manager"]
    user_service = UserService(g.db_session, jwt)

    user = user_service.get_by_id(g.current_user_id)

    if not user:
        return Response(status=401)

    return jsonify(user.to_dict())