from typing import Sequence
from app.models import Contact
from app.repositories import ContactRepository
from sqlalchemy.orm import Session


class ContactService:
    def __init__(self, session: Session) -> None:
        self.repository = ContactRepository(session)

    def create_contact(
        self,
        caller_id: int,
        caller_role: str,
        name: str,
        phone_number: str,
        email: str,
        target_user_id: int | None = None,
    ) -> Contact:

        owner_id = (
            target_user_id
            if (caller_role == "admin" and target_user_id is not None)
            else caller_id
        )

        return self.repository.create_contact(
            name=name,
            phone_number=phone_number,
            email=email,
            user_id=owner_id,
        )

    def get_contact(
        self, contact_id: int, caller_id: int, caller_role: str
    ) -> Contact | None:
        contact = self.repository.find_by_id(contact_id)
        if not contact:
            return None

        if caller_role != "admin" and contact.user_id != caller_id:
            return None

        return contact

    def list_contacts(
        self,
        caller_id: int,
        caller_role: str,
        target_user_id: int | None = None,
    ) -> Sequence[Contact]:
        self.repository.get_all_user_contacts
        if caller_role == "admin" and target_user_id is not None:
            return self.repository.get_all_user_contacts(target_user_id)
        return self.repository.get_all_user_contacts(caller_id)

    def update_contact(
        self,
        contact_id: int,
        caller_id: int,
        caller_role: str,
        name: str | None = None,
        phone_number: str | None = None,
        email: str | None = None,
    ) -> Contact | None:

        contact = self.get_contact(
            contact_id=contact_id,
            caller_id=caller_id,
            caller_role=caller_role,
        )

        if not contact:
            return None

        return self.repository.update_contact(
            contact_id=contact_id, name=name, phone_number=phone_number, email=email
        )

    def delete_contact(
        self, contact_id: int, caller_id: int, caller_role: str
    ) -> Contact | None:
        contact = self.get_contact(
            contact_id=contact_id,
            caller_id=caller_id,
            caller_role=caller_role,
        )

        if not contact:
            return None

        return self.repository.delete_contact(contact_id)
