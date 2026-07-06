from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.repositories.address_repository import AddressRepository
from app.models.address import Address
from .user_service import UserService, UserNotFoundError


class AddressNotFoundError(Exception):
    "Address not found"

    pass


class AddressService:
    def __init__(self, session: Session) -> None:
        self.address_repo = AddressRepository(session)

    def register_new_address(
        self, physical_address: str, user_id: int
    ) -> dict[str, Any]:
        
        user_service = UserService(self.address_repo.session)
        user = user_service.get_user_by_id(user_id)

        if not user:
            raise  UserNotFoundError(f"Unable to find user with ID {user_id}")
        
        new_address = Address(physical_address=physical_address, user_id=user_id)

        self.address_repo.create(new_address)

        self.address_repo.session.flush()

        return {
            "id": new_address.id,
            "user_id": new_address.user_id,
            "physical_address": new_address.physical_address
        }

    def get_address_by_id(self, id: int):
        address = self.address_repo.get_by_id(id)

        if address is None:
            raise AddressNotFoundError(f"Address with id: {id} not found")

        return address.to_dict()
    
    def get_address_with_phrase(self, phrase: str) -> list[dict[str, Any]]:
        addresses = self.address_repo.get_by_address_phrase(phrase)

        if addresses is None:
            return []

        return [address.to_dict() for address in addresses]

    def delete_address_by_id(self, id: int):
        address = self.address_repo.get_by_id(id)
        if address is None:
            raise AddressNotFoundError(f"Address with id: {id} not found")

        address_dict = address.to_dict()

        self.address_repo.delete(address)

        return address_dict

    def get_all_addresses(self) -> list[dict[str, Any]]:
        stmt = select(Address)

        addresss = self.address_repo.session.scalars(stmt).all()

        return [address.to_dict() for address in addresss]

    def update_address(self, address_id: int, data: dict[str, Any]) -> dict[str, Any]:
        address = self.address_repo.get_by_id(address_id)

        if address is None:
            raise AddressNotFoundError(f"Address with ID {address_id} does not exist.")

        address.physical_address = str(data.get("physical_address", address.physical_address))
        address.user_id = int(data.get("user_id", address.user_id))

        self.address_repo.save(address)
        return address.to_dict()
