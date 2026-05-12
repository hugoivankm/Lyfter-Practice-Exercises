from flask import Blueprint, g, request
from services.rental_service import RentalService
from http import HTTPStatus
from .responses import json_response, error_response

rental_bp = Blueprint("rental_bp", __name__)


@rental_bp.route("/", methods=["POST"])
def create_rental():
    raise NotImplementedError()

@rental_bp.route('/', methods=['GET'])
def list_rentals():
    raise NotImplementedError()

@rental_bp.route('/<int:rental_id>', methods=['GET'])
def get_rental(rental_id: int):
    raise NotImplementedError()

@rental_bp.route('/<int:rental_id>', methods=['PATCH'])
def update_rental(rental_id: int):
    raise NotImplementedError()

@rental_bp.route('/<int:rental_id>', methods=['DELETE'])
def delete_rental(rental_id: int):
    raise NotImplementedError()