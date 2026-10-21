from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.invoice import Invoice
from app.models.invoice_detail import InvoiceDetail


class InvoiceRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_invoice(self, user_id: int, items: list[dict[str, Any]]) -> Invoice:
        invoice = Invoice(user_id=user_id)

        for item in items:
            detail = InvoiceDetail(
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
            )
            invoice.details.append(detail)

        self.session.add(invoice)
        self.session.flush()
        return invoice

    def get_invoice_by_id(self, invoice_id: int) -> Invoice | None:
        stmt = (
            select(Invoice)
            .options(selectinload(Invoice.details).joinedload(InvoiceDetail.product))
            .where(Invoice.id == invoice_id)
        )
        return self.session.scalars(stmt).first()

    def get_invoices(self) -> list[Invoice] | None:
        stmt = select(Invoice).options(selectinload(Invoice.details))
        invoices = list(self.session.scalars(stmt).all())
        return invoices if invoices else None

    def get_invoices_by_user(self, user_id: int) -> list[Invoice]:
        stmt = (
            select(Invoice)
            .options(selectinload(Invoice.details))
            .where(Invoice.user_id == user_id)
        )
        return list(self.session.scalars(stmt).all())

    def delete_invoice(self, invoice_id: int) -> Invoice | None:
        invoice = self.get_invoice_by_id(invoice_id)
        if not invoice:
            return None

        self.session.delete(invoice)
        self.session.flush()
        return invoice
