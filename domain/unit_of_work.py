from abc import ABC, abstractmethod
from domain.repositories import ProductRepository, OrderRepository, CustomerRepository, WishlistRepository

class UnitOfWork(ABC):
    @abstractmethod
    def __init__(self, product_repo: ProductRepository, order_repo: OrderRepository, customer_repo: CustomerRepository, wishlist_repo: WishlistRepository):
        self._product_repo=product_repo
        self._order_repo=order_repo
        self._customer_repo=customer_repo
        self._wishlist_repo=wishlist_repo

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exception_type, exception_value, traceback):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @property
    def product_repo(self):
        return self._product_repo

    @product_repo.setter
    def product_repo(self, product_repo: ProductRepository):
        self._product_repo=product_repo

    @property
    def order_repo(self):
        return self._order_repo

    @order_repo.setter
    def order_repo(self, order_repo: OrderRepository):
        self._order_repo=order_repo

    @property
    def customer_repo(self):
        return self._customer_repo

    @customer_repo.setter
    def customer_repo(self, customer_repo: CustomerRepository):
        self._customer_repo=customer_repo

    @property
    def wishlist_repo(self):
        return self._wishlist_repo

    @wishlist_repo.setter
    def wishlist_repo(self, wishlist_repo: WishlistRepository):
        self._wishlist_repo=wishlist_repo