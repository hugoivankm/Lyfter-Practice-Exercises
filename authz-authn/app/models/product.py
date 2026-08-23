from datetime import datetime
from typing import Any, TYPE_CHECKING
from sqlalchemy import String, DateTime, Numeric, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .model import Base

if TYPE_CHECKING:
    from app.models import InvoiceDetail


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    entry_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    quantity: Mapped[int] = mapped_column(Integer, default=0)

    details: Mapped[list["InvoiceDetail"]] = relationship(
        "InvoiceDetail", back_populates="product"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, price={self.price!r}, entry_date={self.entry_date!r}), quantity={self.quantity!r}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "entry_date": self.entry_date,
            "quantity": self.quantity,
        }
