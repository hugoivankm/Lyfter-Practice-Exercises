from flask import Blueprint, jsonify, g, request
from typing import cast, Any
from app.services import InvoiceService
from app.utils.decorators import login_required

invoice_bp = Blueprint("invoices", __name__)

@invoice_bp.route("/create", methods=["POST"])
@login_required
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

        new_invoice = invoice_service.create(
            user_id = user_id,
            items=details
        )

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
        invoices = invoice_service.get_all()
        if invoices is None:
            invoices = []
        return jsonify(invoices), 200
    except Exception as ex:
        print(ex)
        return jsonify({"error": "Something went wrong"}), 500


@invoice_bp.route("/<int:id>", methods=["DELETE"])
@login_required
def delete_invoice(id: int):
   try:
    invoice_service = InvoiceService(g.db_session)
    deleted_invoice = invoice_service.delete(id)
    if not deleted_invoice:
        raise Exception("Unable to delete invoice")
    return deleted_invoice
   except Exception as ex:
       print(ex)
       return jsonify({"error": "Something went wrong"}), 500 