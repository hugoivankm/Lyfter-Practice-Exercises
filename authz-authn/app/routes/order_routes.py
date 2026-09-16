from typing import Any

from app.services import PurchaseService
from app.utils.decorators import login_required
from flask import Blueprint, g, jsonify, request

order_bp = Blueprint("orders", __name__)


@order_bp.route("/", methods=["POST"])
@login_required
def process():
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        raw_data: dict[str, Any] = request.get_json() or {}
        if not isinstance(raw_data, dict):
            raise TypeError("Invalid data format")

        items: list[dict[str, Any]] | None = raw_data.get("items")

        if not isinstance(items, list) or not items:
            return jsonify({"error": "Missing or empty 'items' list"}), 400

        purchase_service = PurchaseService(g.db_session)
        result = purchase_service.process(g.current_user_id, items=items)

        if result is None:
            g.db_session.rollback()
            return jsonify(
                {
                    "error": "Order failed business validation",
                }
            ), 422

        return jsonify(result), 201
    except TypeError as ex:
        g.db_session.rollback()
        return jsonify({"error": str(ex).strip("'\"")}), 400
    except KeyError as ex:
        g.db_session.rollback()
        return jsonify({"error": str(ex).strip("'\"")}), 404
    except ValueError as ex:
        g.db_session.rollback()
        return jsonify({"error": str(ex)}), 422
    except Exception as ex:
        g.db_session.rollback()
        print(ex)
        return jsonify("Something went wrong"), 500
