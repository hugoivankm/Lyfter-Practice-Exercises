from datetime import UTC, datetime
from typing import Any

from app.models.model import Base
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class LoginEntry(Base):
    __tablename__ = "login_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)
    is_success: Mapped[bool] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "ip_address": self.ip_address,
            "is_success": self.is_success,
            "timestamp": self.timestamp.isoformat(),
        }
