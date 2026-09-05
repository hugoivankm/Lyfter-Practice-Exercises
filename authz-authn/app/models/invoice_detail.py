from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .model import Base

if TYPE_CHECKING:
    from .invoice import Invoice
    from .product import Product


class InvoiceDetail(Base):
    __tablename__ = "invoice_details"

    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="details")
    product: Mapped["Product"] = relationship("Product", back_populates="details")

    @property
    def line_total(self) -> float:
        return float(self.unit_price) * self.quantity

    def to_dict(self) -> dict[str, Any]:
        return {
            "product_name": self.product.name,
            "quantity": self.quantity,
            "unit_price": float(self.unit_price),
            "line_total": self.line_total,
        }
