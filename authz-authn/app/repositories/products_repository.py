from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_product(self, name: str, price: float, quantity: int) -> Product:
        product = Product(name=name, price=price, quantity=quantity)
        self.session.add(product)
        self.session.flush()
        return product

    def find_product(self, name: str) -> Product | None:
        return self.session.query(Product).filter(Product.name == name).first()

    def find_product_by_id_and_update(self, product_id: int) -> Product | None:
        stmt = select(Product).where(Product.id == product_id).with_for_update()
        return self.session.scalars(stmt).first()

    def get_products(self) -> list[Product] | None:
        stmt: Select[tuple[Product]] = select(Product)
        products = list(self.session.scalars(stmt).all())
        return products if products else None

    def find_product_by_id(self, product_id: int) -> Product | None:
        return self.session.get(Product, product_id)

    def update_product(
        self, product_id: int, new_quantity: int, new_price: float
    ) -> Product | None:
        product = self.find_product_by_id(product_id)
        if not product:
            return None

        product.price = new_price
        product.quantity = new_quantity
        self.session.flush()
        return product

    def delete_product(self, product_id: int) -> Product | None:
        product = self.find_product_by_id(product_id)
        if not product:
            return None

        self.session.delete(product)
        self.session.flush()
        return product
