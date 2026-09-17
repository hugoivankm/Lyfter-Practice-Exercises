from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.login_entry import LoginEntry


class LoginEntryRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self, user_id: int | None, ip_address: str, is_success: bool
    ) -> LoginEntry:
        entry = LoginEntry(
            user_id=user_id,
            ip_address=ip_address,
            is_success=is_success,
        )

        self.session.add(entry)
        self.session.flush()
        return entry

    def find_all(self, user_id: int | None = None) -> list[LoginEntry]:
        stmt = select(LoginEntry).order_by(LoginEntry.timestamp.desc())

        if user_id is not None:
            stmt = stmt.where(LoginEntry.user_id == user_id)

        return self.session.scalars(stmt).all()
