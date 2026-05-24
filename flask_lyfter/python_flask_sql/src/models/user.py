from enum import StrEnum
from dataclasses import dataclass
from datetime import date
from typing import Tuple, Any, Optional


class AccountStatus(StrEnum):
    CLOSED = "closed"
    ACTIVE = "active"
    DELINQUENT = "delinquent"

@dataclass
class User:
    id: int
    email: str
    username: str
    password: str
    full_name: str
    birthdate: date
    account_status: AccountStatus

    @classmethod
    def from_row(cls, row: Tuple[Any, ...] | None) -> Optional["User"]:
        if not row:
            return None
        return cls(
            id=row[0],
            email=row[1],
            username=row[2],
            password="********",
            full_name=row[4],
            birthdate=row[5],
            account_status=AccountStatus(row[6])
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "password": self.password,
            "full_name": self.full_name,
            "birthdate": self.birthdate.isoformat() if self.birthdate else None,
            "account_status": self.account_status.value
        }