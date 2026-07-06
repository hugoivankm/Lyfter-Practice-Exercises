from typing import Optional, Any, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .model import Base

if TYPE_CHECKING:
    from .user import User

class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    make: Mapped[str] = mapped_column(String(30), nullable=False)
    model: Mapped[str] = mapped_column(String(30), nullable=False)
    year: Mapped[int] = mapped_column(
        Integer,
    )
    vin: Mapped[Optional[str]] = mapped_column(String(17), unique=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    user: Mapped["User"] = relationship(back_populates="vehicles")

    __table_args__ = (
        CheckConstraint("year >= 1886 and year <= 2100", name="check_vehicle_year"),
    )

    def __repr__(self) -> str:
        return f"Vehicle(id={self.id!r}, make={self.make!r}, model={self.model!r}, year={self.year})"
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "vin": self.vin,
            "user_id": self.user_id
        }
    