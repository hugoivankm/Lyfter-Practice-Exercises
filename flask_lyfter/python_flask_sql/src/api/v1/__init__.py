from flask import Blueprint
from .user_routes import user_bp
from .vehicle_routes import vehicle_bp
from .rental_routes import rental_bp

v1_bp = Blueprint("v1", __name__)

v1_bp.register_blueprint(user_bp, url_prefix="/users")
v1_bp.register_blueprint(vehicle_bp, url_prefix="/vehicles")
v1_bp.register_blueprint(rental_bp, url_prefix="/rentals")
