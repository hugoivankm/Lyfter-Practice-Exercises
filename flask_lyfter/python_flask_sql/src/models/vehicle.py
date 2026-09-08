from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any, Optional


class VehicleStatus(StrEnum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    RENTED = "rented"
    IN_MAINTENANCE = "in_maintenance"
    UNAVAILABLE = "unavailable"


@dataclass
class Vehicle:
    id: int
    make: str
    model: str
    model_year: int
    vehicle_status: VehicleStatus

    @classmethod
    def from_row(cls, row: tuple[Any, ...] | None) -> Optional["Vehicle"]:
        if not row:
            return None
        return cls(
            id=row[0],
            make=row[1],
            model=row[2],
            model_year=row[3],
            vehicle_status=row[4],
        )

    def to_dict(self):
        return asdict(self)
