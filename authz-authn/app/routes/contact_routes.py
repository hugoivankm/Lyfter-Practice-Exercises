from typing import cast, Any
from flask import Blueprint, jsonify, g, request

from app.services import ContactService
from app.utils.decorators import login_required

contact_bp = Blueprint("contacts", __name__)


@contact_bp.route("/create", methods=["POST"])
@login_required
def create_contact():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400

    raw_data = request.get_json()
    if not isinstance(raw_data, dict):
        return jsonify(
            {"error": "Invalid JSON format, expected a dictionary object"}
        ), 400

    payload = cast(dict[str, Any], raw_data)
    required_keys = ["name", "phone_number", "email"]

    missing_params: list[str] = [
        field for field in required_keys if field not in payload
    ]
    if missing_params:
        return jsonify(
            {"error": f"Missing fields in contact: {', '.join(missing_params)}"}
        ), 400

    try:
        name = str(payload["name"]).strip()
        if not name:
            raise ValueError("Contact name cannot be empty")

        phone_number = str(payload["phone_number"]).strip()
        if not phone_number:
            raise ValueError("Phone number cannot be empty")

        email = str(payload["email"]).strip()
        if not email:
            raise ValueError("Email cannot be empty")

        target_user_id = payload.get("user_id")
        if target_user_id is not None:
            target_user_id = int(target_user_id)

        contact_service = ContactService(g.db_session)

        new_contact = contact_service.create_contact(
            caller_id=g.current_user_id,
            caller_role=g.current_user_role,
            name=name,
            phone_number=phone_number,
            email=email,
            target_user_id=target_user_id,
        )

        return jsonify(new_contact.to_dict()), 201

    except (ValueError, TypeError) as err:
        return jsonify({"error": f"Invalid field data: {err}"}), 400
    except Exception as ex:
        print(ex)
        return jsonify({"error": "Something went wrong"}), 500


@contact_bp.route("/", methods=["GET"])
@login_required
def list_contacts():
    try:
        requested_user_id = request.args.get("user_id", type=int)

        contact_service = ContactService(g.db_session)
        contacts = contact_service.list_contacts(
            caller_id=g.current_user_id,
            caller_role=g.current_user_role,
            target_user_id=requested_user_id,
        )
        return jsonify([contact.to_dict() for contact in contacts]), 200
    except Exception as ex:
        print(ex)
        return jsonify({"error": "Something went wrong"}), 500


@contact_bp.route("/<int:id>", methods=["GET"])
@login_required
def get_contact(id: int):
    try:
        contact_service = ContactService(g.db_session)
        contact = contact_service.get_contact(
            contact_id=id,
            caller_id=g.current_user_id,
            caller_role=g.current_user_role,
        )
        if not contact:
            return jsonify({"error": "Contact not found"}), 404

        return jsonify(contact.to_dict()), 200
    except Exception as ex:
        print(ex)
        return jsonify({"error": "Something went wrong"}), 500


@contact_bp.route("/<int:id>", methods=["PUT"])
@login_required
def update_contact(id: int):
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400

        raw_data = request.get_json()
        if not isinstance(raw_data, dict):
            return jsonify(
                {"error": "Invalid JSON format, expected a dictionary object"}
            ), 400

        payload = cast(dict[str, Any], raw_data)
        required_keys = ["name", "phone_number", "email"]

        missing_params: list[str] = [
            field for field in required_keys if field not in payload
        ]
        if missing_params:
            return jsonify(
                {"error": f"Missing fields in contact: {', '.join(missing_params)}"}
            ), 400

        name = str(payload["name"]).strip()
        if not name:
            raise ValueError("Contact name cannot be empty")

        phone_number = str(payload["phone_number"]).strip()
        if not phone_number:
            raise ValueError("Phone number cannot be empty")

        email = str(payload["email"]).strip()
        if not email:
            raise ValueError("Email cannot be empty")

        contact_service = ContactService(g.db_session)
        updated_contact = contact_service.update_contact(
            contact_id=id,
            caller_id=g.current_user_id,
            caller_role=g.current_user_role,
            name=name,
            phone_number=phone_number,
            email=email,
        )

        if not updated_contact:
            return jsonify({"error": "Contact not found or access denied"}), 404

        return jsonify(updated_contact.to_dict()), 200

    except (ValueError, TypeError) as err:
        return jsonify({"error": f"Invalid field data: {err}"}), 400
    except Exception as ex:
        print(ex)
        return jsonify({"error": "Something went wrong"}), 500


@contact_bp.route("/<int:id>", methods=["DELETE"])
@login_required
def delete_contact(id: int):
    try:
        contact_service = ContactService(g.db_session)
        deleted_contact = contact_service.delete_contact(
            contact_id=id,
            caller_id=g.current_user_id,
            caller_role=g.current_user_role,
        )
        if not deleted_contact:
            return jsonify({"error": "Contact not found or access denied"}), 404

        return jsonify(deleted_contact.to_dict()), 200
    except Exception as ex:
        print(ex)
        return jsonify({"error": "Something went wrong"}), 500
