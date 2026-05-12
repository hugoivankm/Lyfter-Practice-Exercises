from enum import StrEnum
from dataclasses import dataclass, asdict
from typing import Tuple, Any, Optional


class VehicleStatus(StrEnum):
    AVAILABLE = "available"
    RENTED = "rented"
    IN_MAINTENANCE = "in_maintenance"
    UNAVAILABLE = "unavailable"


@dataclass
class Vehicle:
    id: int
    make: str
    model: str
    model_year: int
    status: VehicleStatus

    @classmethod
    def from_row(cls, row: Tuple[Any, ...] | None) -> Optional["Vehicle"]:
        if not row:
            return None
        return cls(
            id=row[0], make=row[1], model=row[2], model_year=row[3], status=row[4]
        )

    def to_dict(self):
        return asdict(self)
