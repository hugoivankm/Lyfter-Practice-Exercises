from datetime import datetime
from typing import List, Any, Optional, TYPE_CHECKING
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .model import Base

if TYPE_CHECKING:
    from .address import Address
    from .vehicle import Vehicle


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    vehicles: Mapped[List["Vehicle"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, full_name={self.full_name!r}, email={self.email!r}, phone_number={self.phone_number!r})"

    def to_dict(self, view: str = "compact") -> dict[str, Any]:

        # extended view
        if view == "extended":
            return {
                "id": self.id,
                "full_name": self.full_name,
                "email": self.email,
                "phone_number": self.phone_number,
                "addreses": [address.to_dict() for address in self.addresses],
                "vehicles": [vehicle.to_dict() for vehicle in self.vehicles],
            }

        # compact view
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
        }
