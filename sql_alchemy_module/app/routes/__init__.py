from flask import Blueprint
from .user_routes import user_bp

v1_bp = Blueprint('v1', __name__)

v1_bp.register_blueprint(user_bp, url_prefix='/users')