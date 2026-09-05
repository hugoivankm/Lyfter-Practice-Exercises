from typing import Any, cast

from app.services import InvoiceService
from app.utils.decorators import admin_required, login_required
from flask import Blueprint, g, jsonify, request
from werkzeug.exceptions import HTTPException

invoice_bp = Blueprint("invoices", __name__)


@invoice_bp.route("/", methods=["POST"])
@admin_required
def create_invoice():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    raw_data = request.get_json()
    if not isinstance(raw_data, dict):
        return jsonify(
            {"error": "Invalid JSON format, expected a dictionary object"}
        ), 400

    payload = cast(dict[str, Any], raw_data)
    required_keys = ["user_id", "items"]

    missing_params: list[str] = [
        field for field in required_keys if field not in payload
    ]
    if missing_params:
        return jsonify(
            {"error": f"Missing fields in invoice: {', '.join(missing_params)}"}
        ), 400

    try:
        user_id = int(payload["user_id"])
        details = [item for item in payload["items"]]

        invoice_service = InvoiceService(g.db_session)

        new_invoice = invoice_service.create(user_id=user_id, items=details)

        return jsonify(new_invoice), 201

    except (ValueError, TypeError) as err:
        return jsonify({"error": f"Invalid field data: {err}"}), 400
    except Exception as ex:
        print(ex)
        return jsonify({"error": "Something went wrong"}), 500


@invoice_bp.route("/", methods=["GET"])
@login_required
def list_invoices():
    try:
        invoice_service = InvoiceService(g.db_session)
        target_user_id = request.args.get("user_id", type=int)

        current_user_id: int = g.current_user_id
        is_admin: bool = g.current_user_role == "admin"

        invoices = invoice_service.get_all(
            target_user_id=target_user_id,
            current_user_id=current_user_id,
            is_admin=is_admin,
        )
        return jsonify(invoices), 200
    except HTTPException as http_ex:
        return jsonify({"error": http_ex.description}), http_ex.code
    except Exception:
        return jsonify({"error": "Something went wrong"}), 500


@invoice_bp.route("/<int:id>", methods=["GET"])
@login_required
def get_invoice_by_id(id: int):
    try:
        invoice_service = InvoiceService(g.db_session)
        current_user_id: int = g.current_user_id
        is_admin: bool = (g.current_user_role == "admin")

        retrieved_invoice = invoice_service.get_by_id(
            invoice_id=id,
            current_user_id=current_user_id,
            is_admin=is_admin,
        )
        return jsonify(retrieved_invoice), 200
    except HTTPException as http_ex:
        return jsonify({"error": http_ex.description}), http_ex.code
    except Exception:
        return jsonify({"error": "Something went wrong"}), 500


@invoice_bp.route("/<int:id>", methods=["DELETE"])
@admin_required
def delete_invoice(id: int):
    try:
        invoice_service = InvoiceService(g.db_session)
        deleted_invoice = invoice_service.delete(id)
        return jsonify(deleted_invoice), 200
    except HTTPException as http_ex:
        return jsonify({"error": http_ex.description}), http_ex.code
    except Exception as ex:
        print(ex)
        return jsonify({"error": "Something went wrong"}), 500
