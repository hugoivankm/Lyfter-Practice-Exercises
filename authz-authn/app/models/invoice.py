from typing import Any, TYPE_CHECKING
from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .model import Base

if TYPE_CHECKING:
    from .user import User
    from .invoice_detail import InvoiceDetail

class Invoice(Base):
    __tablename__ = "invoices"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    
    user: Mapped["User"] = relationship("User", back_populates="invoices")
    details: Mapped[list["InvoiceDetail"]] = relationship(
        "InvoiceDetail", back_populates="invoice", cascade="all, delete-orphan"
    )

    @property
    def total_amount(self) -> float:
        return sum(detail.line_total for detail in self.details)
    
    def __repr__(self) -> str:
        return f"Invoice(id={self.id!r}, user_id={self.user_id!r}, date={self.date!r})"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "date": self.date.isoformat() if self.date else None,
            "total_amount": self.total_amount,
            "details": [detail.to_dict() for detail in self.details],
        }
    