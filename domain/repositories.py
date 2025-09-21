from abc import ABC, abstractmethod
from typing import List
from .models import Product, Order, Customer, Wishlist

class ProductRepository(ABC):
    @abstractmethod
    def add(self, product: Product):
        pass

    @abstractmethod
    def get(self, product_id: int) -> Product:
        pass

    @abstractmethod
    def list(self, ids: List[int] = None) -> List[Product]:
        pass

    @abstractmethod
    def update(self, product_id: int, product: Product):
        pass

    @abstractmethod
    def delete(self, product_id: int):
        pass

class CustomerRepository(ABC):
    @abstractmethod
    def add(self, customer: Customer):
        pass

    @abstractmethod
    def get(self, customer_id: int) -> Customer:
        pass

    @abstractmethod
    def list(self, ids: List[int] = None) -> List[Customer]:
        pass

    @abstractmethod
    def update(self, customer_id: int, customer: Customer):
        pass

    @abstractmethod
    def delete(self, customer_id: int):
        pass

class WishlistRepository(ABC):
    @abstractmethod
    def add(self, wishlist: Wishlist):
        pass

    @abstractmethod
    def get(self, wishlist_id: int) -> Wishlist:
        pass

    @abstractmethod
    def list(self, ids: List[int] = None) -> List[Wishlist]:
        pass

    @abstractmethod
    def update(self, wishlist_id: int, wishlist: Wishlist):
        pass

    @abstractmethod
    def delete(self, wishlist_id: int):
        pass

class OrderRepository(ABC):
    @abstractmethod
    def add(self, order: Order):
        pass

    @abstractmethod
    def get(self, order_id: int) -> Order:
        pass

    @abstractmethod
    def list(self, ids: List[int] = None) -> List[Order]:
        pass

    @abstractmethod
    def update(self, order_id: int, order: Order):
        pass

    @abstractmethod
    def delete(self, order_id: int):
        pass