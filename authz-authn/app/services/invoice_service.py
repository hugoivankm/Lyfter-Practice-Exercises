from typing import Any

from app.repositories import InvoiceRepository
from sqlalchemy.orm import Session


class InvoiceService:
    def __init__(self, session: Session) -> None:
        self.repo = InvoiceRepository(session)

    def create(
        self, user_id: int, items: list[dict[str, Any]]
    ) -> dict[str, Any] | None:
        invoice = self.repo.create_invoice(user_id, items)
        if not invoice:
            return None
        return invoice.to_dict()

    def get_by_id(self, id: int) -> dict[str, Any] | None:
        invoice = self.repo.get_invoice_by_id(id)
        if not invoice:
            return None
        return invoice.to_dict()

    def get_by_user_id(self, user_id: int) -> list[dict[str, Any]] | None:
        invoices = self.repo.get_invoices_by_user(user_id)
        if not invoices:
            return None
        return [invoice.to_dict() for invoice in invoices]

    def get_all(self) -> list[dict[str, Any]] | None:
        invoices = self.repo.get_invoices()
        if not invoices:
            return None
        return [invoice.to_dict() for invoice in invoices]

    def delete(self, id: int) -> dict[str, Any] | None:
        invoice = self.repo.get_invoice_by_id(id)
        if not invoice:
            return None

        data = invoice.to_dict()
        self.repo.delete_invoice(id)

        return data
