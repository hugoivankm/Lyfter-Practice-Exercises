
from app.models import User
from app.models.vehicle import Vehicle
from sqlalchemy import func, select
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def create(self, user: User) -> User:
        self.session.add(user)
        return user

    def delete(self, user: User):
        self.session.delete(user)

    def save(self, user: User) -> User:
        self.session.add(user)
        return user

    def get_by_vehicle_count(self, count: int, or_more: bool = False) -> list[User]:

        vehicle_count_subquery = (
            select(func.count()).where(Vehicle.user_id == User.id).scalar_subquery()
        )

        if or_more:
            stmt = select(User).where(vehicle_count_subquery >= count)
        else:
            stmt = select(User).where(vehicle_count_subquery == count)
        return list(self.session.scalars(stmt).all())
