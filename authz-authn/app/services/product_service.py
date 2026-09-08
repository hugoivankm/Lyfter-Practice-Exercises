from typing import Any

from app.repositories import ProductRepository
from sqlalchemy.orm import Session


class ProductService:
    def __init__(self, session: Session) -> None:
        self.repo = ProductRepository(session)

    def register(self, name: str, price: float, quantity: int) -> dict[str, Any] | None:
        product = self.repo.create_product(name, price, quantity)
        return product.to_dict()

    def get_by_id(self, id: int) -> dict[str, Any] | None:
        product = self.repo.find_product_by_id(id)
        if not product:
            return None
        return product.to_dict()

    def get_all(self) -> list[dict[str, Any]]:
        products = self.repo.get_products()
        if not products:
            return []
        return [p.to_dict() for p in products]

    def update(self, id: int, price: float, quantity: int) -> dict[str, Any] | None:
        updated_product = self.repo.update_product(id, quantity, price)
        if not updated_product:
            return None
        return updated_product.to_dict()

    def delete(self, id: int) -> dict[str, Any] | None:
        deleted_product = self.repo.delete_product(id)
        if not deleted_product:
            return None
        return deleted_product.to_dict()
