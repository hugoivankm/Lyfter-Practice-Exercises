from typing import Any

from app.repositories import InvoiceRepository, ProductRepository
from app.services.payment_service import PaymentService
from sqlalchemy.orm import Session


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
            try:
                if not isinstance(item, dict):
                    raise TypeError(f"item is not a dict {type(item).__name__}")

                raw_id = item.get("product_id")
                raw_qty = item.get("quantity")

                if not isinstance(raw_id, int) or isinstance(raw_id, bool):
                    raise TypeError("product_id is not an integer value")

                if not isinstance(raw_qty, int) or isinstance(raw_qty, bool):
                    raise TypeError("quantity is not an integer")

                product_id: int | None = int(item.get("product_id", -1))
                qty: int = int(item.get("quantity", 0))

                if not product_id or qty <= 0:
                    raise ValueError("invalid value for product_id or quantity")
            except (TypeError, ValueError) as ex:
                raise ValueError("product_id and quantity must be integers") from ex

            product = self.product_repo.find_product_by_id_and_update(product_id)
            if not product or product.quantity < qty:
                raise ValueError(
                    f"invalid item details: product_id={product_id}, quantity={qty}."
                )

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
