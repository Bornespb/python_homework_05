from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic
from .models import Product, Order, Customer, Wishlist

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    def add(self, entity: T):
        pass
    
    @abstractmethod
    def get(self, id: int) -> T:
        pass

    @abstractmethod
    def list(self, ids: List[int] | None = None) -> List[T]:
        pass

    @abstractmethod
    def update(self, id: int, entity: T):
        pass

    @abstractmethod
    def delete(self, id: int):
        pass

class ProductRepository(BaseRepository[Product]):
    pass

class CustomerRepository(BaseRepository[Customer]):
    pass

class WishlistRepository(BaseRepository[Wishlist]):
    pass

class OrderRepository(BaseRepository[Order]):
    pass