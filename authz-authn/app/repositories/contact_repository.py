from typing import Sequence
from app.models import Contact
from sqlalchemy import select
from sqlalchemy.orm import Session


class ContactRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_contact(
        self, name: str, phone_number: str, email: str, user_id: int
    ) -> Contact:
        contact = Contact(
            name=name, phone_number=phone_number, email=email, user_id=user_id
        )
        self.session.add(contact)
        self.session.flush()
        return contact

    def find_by_name(self, contact_name: str, user_id: int) -> Sequence[Contact]:
        stmt = select(Contact).where(
            Contact.name == contact_name, Contact.user_id == user_id
        )
        return self.session.scalars(stmt).all()

    def find_by_id(self, contact_id: int) -> Contact | None:
        stmt = select(Contact).where(Contact.id == contact_id)
        return self.session.scalars(stmt).first()

    def get_all_user_contacts(self, user_id: int) -> Sequence[Contact]:
        stmt = select(Contact).where(Contact.user_id == user_id)
        return self.session.scalars(stmt).all()

    def update_contact(
        self,
        contact_id: int,
        name: str | None,
        phone_number: str | None,
        email: str | None,
    ) -> Contact | None:
        contact = self.find_by_id(contact_id)
        if not contact:
            return None

        if name is not None:
            contact.name = name
        if phone_number is not None:
            contact.phone_number = phone_number
        if email is not None:
            contact.email = email

        self.session.flush()
        return contact

    def delete_contact(self, contact_id: int) -> Contact | None:
        contact = self.find_by_id(contact_id)
        if not contact:
            return None

        self.session.delete(contact)
        self.session.flush()
        return contact
