import random
from typing import Any

from app.repositories.login_entry_repository import LoginEntryRepository
from sqlalchemy.orm import Session


class LoginEntryService:

    def __init__(self, session: Session):
        self.repo = LoginEntryRepository(session)

    def _generate_fake_ip(self) -> str:
        """Simulate a standard random public IPv4 address."""
        return f"{random.randint(11, 199)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"

    def record_entry(
            self,
            user_id: int | None,
            is_success: bool,
            ip_address: str | None = None,
    ) -> dict[str, Any]:

        client_ip = ip_address or self._generate_fake_ip()

        entry = self.repo.create(
            user_id=user_id,
            ip_address=client_ip,
            is_success=is_success
        )

        return entry.to_dict()

    def get_history(self, user_id: int | None = None) -> list[dict[str, Any]]:
        entries = self.repo.find_all(user_id)
        return [entry.todict() for entry in entries]