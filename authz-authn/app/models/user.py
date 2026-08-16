from datetime import datetime
from typing import Any, List, TYPE_CHECKING
from sqlalchemy import String, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .model import Base
if TYPE_CHECKING:
    from .invoice import Invoice

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    role = mapped_column(Enum("admin", "standard", name="user_role"))


    invoices: Mapped[List["Invoice"]] = relationship("Invoice", back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username}, password={'********'})"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "role": self.role,
            "username": self.username,
            "password": "********",
        }
