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
        if product in self.products:
            self.products[self.products.index(product)].quantity += 1
        else:
            self.products.append(product)

    def checkout(self) -> float:
        return sum(product.price * product.quantity for product in self.products)

@dataclass
class Wishlist:
    id: int
    customer: Customer
    products: List[Product] = field(default_factory=list)

    def add_product(self, product: Product) -> None:
        if product in self.products:
            self.products[self.products.index(product)].quantity += 1
        else:
            self.products.append(product)
