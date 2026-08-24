from typing import Any

from sqlalchemy.orm import Session

from app.repositories import InvoiceRepository, ProductRepository
from app.services.payment_service import PaymentService


class PurchaseService:
    def __init__(self, session: Session) -> None:
        self.product_repo = ProductRepository(session)
        self.invoice_repo = InvoiceRepository(session)

    def process(
        self,
        user_id: int,
        items: list[dict[str, Any]],
        card_number: str = "1111-2222-3333-4444",
    ) -> dict[str, Any] | None:
        if not items:
            return None
        total_amount = 0.0
        validated_items: list[dict[str, Any]] = []

        for item in items:
            product_id: int | None = item.get("product_id")
            qty = item.get("quantity", 0)

            if not product_id or qty <= 0:
                return None

            product = self.product_repo.find_product_by_id_and_update(product_id)
            if not product or product.quantity < qty:
                return None

            unit_price = float(product.price)
            total_amount += unit_price * qty

            product.quantity -= qty

            validated_items.append(
                {
                    "product_id": product.id,
                    "quantity": qty,
                    "unit_price": unit_price,
                }
            )

        payment_success, _ = PaymentService.process_payment(total_amount, card_number)
        if not payment_success:
            return None

        invoice = self.invoice_repo.create_invoice(user_id, validated_items)
        if not invoice:
            return None

        return invoice.to_dict()
