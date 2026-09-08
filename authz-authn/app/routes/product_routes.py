from typing import Any, cast

from app.services import ProductService
from app.utils.decorators import admin_required, login_required
from flask import Blueprint, g, jsonify, request
from werkzeug.exceptions import NotFound

product_bp = Blueprint("products", __name__)


@product_bp.route("/", methods=["POST"])
@admin_required
def create_product():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    raw_data = request.get_json()
    if not isinstance(raw_data, dict):
        return jsonify(
            {"error": "Invalid JSON format, expected a dictionary object"}
        ), 400

    payload = cast(dict[str, Any], raw_data)
    required_keys = ["name", "price", "quantity"]

    missing_params: list[str] = [
        field for field in required_keys if field not in payload
    ]
    if missing_params:
        return jsonify(
            {"error": f"Missing fields in product: {', '.join(missing_params)}"}
        ), 400

    try:
        name = str(payload["name"]).strip()
        if not name:
            raise ValueError("Product name cannot be empty")

        price = float(payload["price"])
        if price < 0:
            raise ValueError("Price must be greater than 0")

        quantity = int(payload["quantity"])
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        product_service = ProductService(g.db_session)

        new_product = product_service.register(
            name=name,
            price=price,
            quantity=quantity,
        )

        return jsonify(new_product), 201

    except (ValueError, TypeError) as err:
        return jsonify({"error": f"Invalid field data: {err}"}), 400
    except Exception as ex:
        print(ex)
        return jsonify({"error": "Something went wrong"}), 500


@product_bp.route("/", methods=["GET"])
@login_required
def list_products():
    try:
        product_service = ProductService(g.db_session)
        products = product_service.get_all()
        return jsonify(products), 200
    except Exception as ex:
        print(ex)
        return jsonify({"error": "Something went wrong"}), 500


@product_bp.route("/<int:id>", methods=["PUT"])
@admin_required
def update_product(id: int):
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        raw_data = request.get_json()
        if not isinstance(raw_data, dict):
            return jsonify(
                {"error": "Invalid JSON format, expected a dictionary object"}
            ), 400

        payload = cast(dict[str, Any], raw_data)
        required_keys = ["price", "quantity"]

        missing_params: list[str] = [
            field for field in required_keys if field not in payload
        ]
        if missing_params:
            return jsonify(
                {"error": f"Missing fields in product: {', '.join(missing_params)}"}
            ), 400

        price = float(payload["price"])
        if price < 0:
            raise ValueError("Price must be greater than 0")

        quantity = int(payload["quantity"])

        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        product_service = ProductService(g.db_session)
        update_product = product_service.update(id=id, price=price, quantity=quantity)
        if not update_product:
            raise NotFound()
        return jsonify(update_product), 200
    except NotFound as ex:
        print(ex)
        return jsonify({"error": "product not found"}), 404
    except ValueError as ex:
        print(ex)
        return jsonify({"error": "invalid value in request"}), 400
    except Exception as ex:
        print(ex)
        return jsonify({"error": "Something went wrong"}), 500


@product_bp.route("/<int:id>", methods=["DELETE"])
@admin_required
def delete_product(id: int):
    try:
        product_service = ProductService(g.db_session)
        deleted_product = product_service.delete(id)
        if not deleted_product:
            raise NotFound("Unable to delete product")
        return jsonify(deleted_product), 200
    except NotFound as nfe:
        return jsonify({"error": f"{nfe.description}"}), 404
    except Exception as ex:
        print(ex)
        return jsonify({"error": "Something went wrong"}), 500
