from dataclasses import dataclass, asdict
from typing import Tuple, Any, Optional
from datetime import date
from enum import StrEnum


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
    def from_row(cls, row: Tuple[Any, ...] | None) -> Optional["Rental"]:
        if not row:
            return None
        return cls(
            id=row[0], users_id=row[1], vehicles_id=row[2], rental_date=row[3], rental_status=row[4]
        )

    def to_dict(self):
        return asdict(self)
