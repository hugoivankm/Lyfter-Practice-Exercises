from typing import Any, Dict, List
from flask import Blueprint, jsonify, g, request
from app.services import PurchaseService
from app.utils.decorators import login_required


order_bp = Blueprint("orders", __name__)


@order_bp.route("/process", methods=["POST"])
@login_required
def process():
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        raw_data: Dict[str, Any] = request.get_json() or {}

        items: List[Dict[str, Any]] | None = raw_data.get("items")

        if not isinstance(items, list) or not items:
            return jsonify({"error": "Missing or empty 'items' list"}), 400

        purchase_service = PurchaseService(g.db_session)
        result = purchase_service.process(g.current_user_id, items=items)

        if result is None:
            return jsonify(
                {
                    "error": "Order failed business validation",
                    "reasons": ["Product out of stock"],
                }
            ), 422

        return jsonify(result), 201

    except Exception as ex:
        print(ex)
        return jsonify("Something went wrong"), 500
