from dataclasses import dataclass
from datetime import date
from enum import StrEnum
from typing import Any, Optional


class RentalStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    READY_FOR_PICKUP = "ready_for_pickup"
    ACTIVE = "active"
    OVERDUE = "overdue"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


@dataclass
class Rental:
    id: int
    users_id: int
    vehicles_id: int
    rental_date: date
    rental_status: RentalStatus

    @classmethod
    def from_row(cls, row: tuple[Any, ...] | None) -> Optional["Rental"]:
        if not row:
            return None
        return cls(
            id=row[0],
            users_id=row[1],
            vehicles_id=row[2],
            rental_date=row[3],
            rental_status=row[4],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "users_id": self.users_id,
            "vehicles_id": self.vehicles_id,
            "rental_date": self.rental_date.isoformat() if self.rental_date else None,
            "rental_status": self.rental_status,
        }
