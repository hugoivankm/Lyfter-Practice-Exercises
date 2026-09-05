from typing import Any

from app.repositories import InvoiceRepository
from sqlalchemy.orm import Session
from werkzeug.exceptions import Forbidden, NotFound


class InvoiceService:
    def __init__(self, session: Session) -> None:
        self.repo = InvoiceRepository(session)
        self.session = session

    def create(
        self, user_id: int, items: list[dict[str, Any]]
    ) -> dict[str, Any]:
        invoice = self.repo.create_invoice(user_id, items)
        if not invoice:
            raise RuntimeError("Failed to create invoice in database.")
        return invoice.to_dict()

    def get_by_id(
        self, invoice_id: int, current_user_id: int, is_admin: bool = False
    ) -> dict[str, Any]:
        invoice = self.repo.get_invoice_by_id(invoice_id)
        if not invoice:
            raise NotFound(f"Invoice with ID {invoice_id} not found.")

        if not is_admin and invoice.user_id != current_user_id:
            raise Forbidden("Not enough permissions to view this invoice.")

        return invoice.to_dict()

    def get_by_user_id(self, user_id: int) -> list[dict[str, Any]]:
        invoices = self.repo.get_invoices_by_user(user_id) or []
        return [invoice.to_dict() for invoice in invoices]

    def get_all(
        self, target_user_id: int | None, current_user_id: int, is_admin: bool = False
    ) -> list[dict[str, Any]]:
        if not is_admin:
            target_user_id = current_user_id
        elif target_user_id is None:
            invoices = self.repo.get_invoices() or []
            return [inv.to_dict() for inv in invoices]

        invoices = self.repo.get_invoices_by_user(target_user_id) or []
        return [inv.to_dict() for inv in invoices]

    def delete(self, invoice_id: int) -> dict[str, Any]:
        invoice = self.repo.get_invoice_by_id(invoice_id)
        if not invoice:
            raise NotFound(f"Unable to find invoice {invoice_id} for deletion.")

        data = invoice.to_dict()
        self.repo.delete_invoice(invoice_id)

        return data