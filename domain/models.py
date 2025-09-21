from dataclasses import dataclass, field
from typing import List

@dataclass
class Product:
    id: int
    name: str
    quantity: int
    price: float

@dataclass
class Customer:
    id: int
    name: str

@dataclass
class Order:
    id: int
    customer: Customer
    products: List[Product] = field(default_factory=list)

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def checkout(self) -> int:
        return sum(product.price for product in self.products)

@dataclass
class Wishlist:
    id: int
    customer: Customer
    products: List[Product] = field(default_factory=list)

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def create_order(self) -> Order:
        return Order(customer=self.customer, products=self.products)
