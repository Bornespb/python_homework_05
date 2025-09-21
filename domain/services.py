from typing import List, TypeVar, Generic, Any, Type
from collections.abc import Callable
from .models import Product, Order, Customer, Wishlist
from .unit_of_work import UnitOfWork
from .repositories import BaseRepository

T = TypeVar('T')

class BaseService(Generic[T]):
    def __init__(self, uow: UnitOfWork, repo: BaseRepository[T], model: Type[T]):
        self.uow=uow
        self.repo=repo
        self.model=model

    def create(self, **kwargs) -> T:
        entity=self.model(**kwargs)
        self.repo.add(entity)
        self.uow.commit()
        return entity
    
    def get(self, id: int) -> T:
        return self.repo.get(id)

    def list(self, ids: List[int] | None = None) -> List[T]:
        return self.repo.list(ids)
    
    def update(self, id: int, entity: T) -> T:
        self.repo.update(id, entity)
        self.uow.commit()
        return entity
    
    def delete(self, id: int):
        self.repo.delete(id)
        self.uow.commit()

class ProductService(BaseService[Product]):
    def __init__(self, uow: UnitOfWork):
        super().__init__(uow, uow.product_repo, Product)

class CustomerService(BaseService[Customer]):
    def __init__(self, uow: UnitOfWork):
        super().__init__(uow, uow.customer_repo, Customer)

class WishlistService(BaseService[Wishlist]):
    def __init__(self, uow: UnitOfWork):
        super().__init__(uow, uow.wishlist_repo, Wishlist)

    def add_product_to_wishlist(self, wishlist_id: int, product: Product):
        wishlist=self.get(wishlist_id)
        wishlist.add_product(product)
        self.update(wishlist_id, wishlist)
        self.uow.commit()
        return wishlist

    def create_order_from_wishlist(self, wishlist_id: int, order_id: int):
        wishlist=self.get(wishlist_id)
        order=Order(id=order_id, customer=wishlist.customer, products=wishlist.products)
        self.uow.order_repo.add(order)
        self.uow.commit()
        return order

class OrderService(BaseService[Order]):
    def __init__(self, uow: UnitOfWork):
        super().__init__(uow, uow.order_repo, Order)

    def checkout_order(self, order_id: int) -> float:
        order=self.get(order_id)
        return order.checkout()
    
    def add_product_to_order(self, order_id: int, product: Product):
        order=self.get(order_id)
        order.add_product(product)
        self.update(order_id, order)
        self.uow.commit()
        return order
