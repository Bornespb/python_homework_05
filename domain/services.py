from typing import List
from .models import Product, Order, Customer, Wishlist
from .repositories import ProductRepository, OrderRepository, CustomerRepository, WishlistRepository
from .unit_of_work import UnitOfWork

class ProductService:
    def __init__(self, uow: UnitOfWork):
        self.uow=uow

    def create_product(self, id: int, name: str, quantity: int, price: float) -> Product:
        product=Product(id=id, name=name, quantity=quantity,price=price)
        self.uow.product_repo.add(product)
        self.uow.commit()
        return product

    def get_product(self, product_id: int) -> Product:
        return self.uow.product_repo.get(product_id)

    def list_products(self, ids: List[int] = None) -> List[Product]:
        return self.uow.product_repo.list(ids)

    def update_product(self, product_id: int, product: Product):
        self.uow.product_repo.update(product_id, product)
        self.uow.commit()
        return self.uow.product_repo.get(product_id)

    def delete_product(self, product_id: int):
        self.uow.product_repo.delete(product_id)
        self.uow.commit()

class CustomerService:
    def __init__(self, uow: UnitOfWork):
        self.uow=uow

    def create_customer(self, id: int, name: str) -> Customer:
        customer=Customer(id=id, name=name)
        self.uow.customer_repo.add(customer)
        self.uow.commit()
        return customer

    def get_customer(self, customer_id: int) -> Customer:
        return self.uow.customer_repo.get(customer_id)

    def list_customers(self, ids: List[int] = None) -> List[Customer]:
        return self.uow.customer_repo.list(ids)

    def update_customer(self, customer_id: int, customer: Customer):
        self.uow.customer_repo.update(customer_id, customer)
        self.uow.commit()
        return self.uow.customer_repo.get(customer_id)

    def delete_customer(self, customer_id: int):
        self.uow.customer_repo.delete(customer_id)
        self.uow.commit()

class WishlistService:
    def __init__(self, uow: UnitOfWork):
        self.uow=uow

    def create_wishlist(self, id: int, customer: Customer) -> Wishlist:
        wishlist=Wishlist(id=id, customer=customer)
        self.uow.wishlist_repo.add(wishlist)
        self.uow.commit()
        return wishlist
    
    def get_wishlist(self, wishlist_id: int) -> Wishlist:
        return self.uow.wishlist_repo.get(wishlist_id)

    def list_wishlists(self, ids: List[int] = None) -> List[Wishlist]:
        return self.uow.wishlist_repo.list(ids)
    
    def update_wishlist(self, wishlist_id: int, wishlist: Wishlist):
        self.uow.wishlist_repo.update(wishlist_id, wishlist)
        self.uow.commit()
        return self.uow.wishlist_repo.get(wishlist_id)

    def delete_wishlist(self, wishlist_id: int):
        self.uow.wishlist_repo.delete(wishlist_id)
        self.uow.commit()

    def add_product_to_wishlist(self, wishlist_id: int, product: Product):
        wishlist=self.uow.wishlist_repo.get(wishlist_id)
        wishlist.add_product(product)
        self.uow.wishlist_repo.add(wishlist)
        self.uow.commit()
        return wishlist

class OrderService:
    def __init__(self, uow: UnitOfWork):
        self.uow=uow

    def create_order(self, id: int, customer: Customer, products: List[Product]) -> Order:
        order=Order(id=id, customer=customer, products=products)
        self.uow.order_repo.add(order)
        self.uow.commit()
        return order

    def get_order(self, order_id: int) -> Order:
        return self.uow.order_repo.get(order_id)

    def list_orders(self, ids: List[int] = None) -> List[Order]:
        return self.uow.order_repo.list(ids)

    def update_order(self, order_id: int, order: Order):
        self.uow.order_repo.update(order_id, order)
        self.uow.commit()
        return self.uow.order_repo.get(order_id)

    def delete_order(self, order_id: int):
        self.uow.order_repo.delete(order_id)
        self.uow.commit()

    def checkout_order(self, order_id: int) -> int:
        order=self.uow.order_repo.get(order_id)
        self.uow.commit()
        return order.checkout()
    
    def add_product_to_order(self, order_id: int, product: Product):
        order=self.uow.order_repo.get(order_id)
        order.add_product(product)
        self.uow.order_repo.add(order)
        self.uow.commit()
        return order
