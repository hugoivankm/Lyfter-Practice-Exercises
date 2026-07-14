from datetime import datetime
from typing import Any
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .model import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(64), nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username}, password={'********'})"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "password": "********"
        }
