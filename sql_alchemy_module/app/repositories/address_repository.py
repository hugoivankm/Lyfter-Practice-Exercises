from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import Address


class AddressRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, address_id: int) -> Optional[Address]:
        return self.session.get(Address, address_id)

    def create(self, address: Address) -> Address:
        self.session.add(address)
        return address

    def delete(self, address: Address):
        self.session.delete(address)

    def save(self, address: Address) -> Address:
        self.session.add(address)
        return address
    
    def get_by_address_phrase(self, phrase: str = "") -> list[Address] | None:
        pattern = f"%{phrase}%"

        stmt = select(Address).where(Address.physical_address.ilike(pattern))

        return list(self.session.scalars(stmt).all())

