from typing import List
from sqlalchemy.orm import Session
from domain.models import Order, Product, Customer, Wishlist
from domain.repositories import ProductRepository, OrderRepository, CustomerRepository, WishlistRepository
from .orm import ProductORM, OrderORM, CustomerORM, WishlistORM, WishlistProductORM, OrderProductORM

class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session=session

    def add(self, product:Product):
        product_orm = ProductORM(
            name=product.name,
            quantity=product.quantity,
            price=product.price,
        )
        self.session.add(product_orm)

    def get(self, product_id: int)->Product:
        product_orm= self.session.query(ProductORM).filter_by(id=product_id).one()
        return Product(
            id=product_orm.id,
            name=product_orm.name,
            quantity=product_orm.quantity,
            price=product_orm.price
        )

    def list(self, ids: List[int] | None = None) -> List[Product]:
        query=self.session.query(ProductORM)
        if ids:
            query=query.filter(ProductORM.id.in_(ids))
        products_orm= query.all()
        return [
            Product(id=p.id, name=p.name, quantity=p.quantity, price=p.price)
            for p in products_orm
        ]

    def update(self, product_id: int, product: Product):
        product_orm= self.session.query(ProductORM).filter_by(id=product_id).one()
        product_orm.name=product.name
        product_orm.quantity=product.quantity
        product_orm.price=product.price
        self.session.add(product_orm)
        return self.get(product_id)
        
    def delete(self, product_id: int):
        product_orm= self.session.query(ProductORM).filter_by(id=product_id).one()
        self.session.delete(product_orm)

class SqlAlchemyCustomerRepository(CustomerRepository):
    def __init__(self, session: Session):
        self.session=session

    def add(self, customer: Customer):
        customer_orm = CustomerORM(name=customer.name)
        self.session.add(customer_orm)

    def get(self, customer_id: int)->Customer:
        customer_orm= self.session.query(CustomerORM).filter_by(id=customer_id).one()
        return Customer(id=customer_orm.id, name=customer_orm.name)

    def list(self, ids: List[int] | None = None) -> List[Customer]:
        query=self.session.query(CustomerORM)
        if ids:
            query=query.filter(CustomerORM.id.in_(ids))
        customers_orm= query.all()
        return [
            Customer(id=c.id, name=c.name)
            for c in customers_orm
        ]

    def update(self, customer_id: int, customer: Customer):
        customer_orm= self.session.query(CustomerORM).filter_by(id=customer_id).one()
        customer_orm.name=customer.name
        self.session.add(customer_orm)
        return self.get(customer_id)

    def delete(self, customer_id: int):
        customer_orm= self.session.query(CustomerORM).filter_by(id=customer_id).one()
        self.session.delete(customer_orm)

class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session):
        self.session=session

    def add(self, order:Order):
        order_orm = OrderORM(
            customer_id=order.customer.id,
        )
        order_orm.customer = self.session.query(CustomerORM).filter_by(id=order.customer.id).one()

        product_orms = [
            self.session.query(ProductORM).filter_by(id=p.id).one() for p in order.products
        ]
        order_orm.products = [
            OrderProductORM(product=product_orms[i], order_id=order_orm.id) for i in range(len(product_orms))
        ]
        self.session.add(order_orm)

    def get(self, order_id: int)->Order:
        order_orm= self.session.query(OrderORM).filter_by(id=order_id).one()
        products = [
            Product(id=p.product.id, name=p.product.name, quantity=p.product.quantity, price=p.product.price)
            for p in order_orm.products
        ]
        return Order(
            id=order_orm.id,
            customer= Customer(id=order_orm.customer.id, name=order_orm.customer.name),
            products=products
        )

    def list(self, ids: List[int] | None = None) -> List[Order]:
        query=self.session.query(OrderORM)
        if ids:
            query=query.filter(OrderORM.id.in_(ids))
        orders_orm= query.all()
        orders=[]
        for order_orm in orders_orm:
            products = [
                Product(id=p.product.id, name=p.product.name, quantity=p.product.quantity, price=p.product.price)
                for p in order_orm.products
            ]
            orders.append(Order(id=order_orm.id, customer= Customer(id=order_orm.customer.id, name=order_orm.customer.name), products=products))
        return orders
    
    def update(self, order_id: int, order: Order):
        order_orm= self.session.query(OrderORM).filter_by(id=order_id).one()
        product_orms = [
            self.session.query(ProductORM).filter_by(id=p.id).one() for p in order.products
        ]
        order_orm.products = [
            OrderProductORM(product=i, order_id=order_orm.id) for i in product_orms
        ]
        self.session.add(order_orm)
        return self.get(order_id)
    
    def delete(self, order_id: int):
        order_orm= self.session.query(OrderORM).filter_by(id=order_id).one()
        self.session.delete(order_orm)

class SqlAlchemyWishlistRepository(WishlistRepository):
    def __init__(self, session: Session):
        self.session=session

    def add(self, wishlist: Wishlist):
        wishlist_orm = WishlistORM()
        wishlist_orm.customer = self.session.query(CustomerORM).filter_by(id=wishlist.customer.id).one()
        product_orms = [
            self.session.query(ProductORM).filter_by(id=p.id).one() for p in wishlist.products
        ]
        wishlist_orm.products = [
            WishlistProductORM(product=i, wishlist_id=wishlist_orm.id) for i in product_orms
            for p in wishlist.products
        ]
        self.session.add(wishlist_orm)

    def get(self, wishlist_id: int)->Wishlist:
        wishlist_orm= self.session.query(WishlistORM).filter_by(id=wishlist_id).one()
        products = [
            Product(id=p.product.id, name=p.product.name, quantity=p.product.quantity, price=p.product.price)
            for p in wishlist_orm.products
        ]
        return Wishlist(id=wishlist_orm.id, customer=Customer(id=wishlist_orm.customer.id, name=wishlist_orm.customer.name), products=products)
    
    def list(self, ids: List[int] | None = None) -> List[Wishlist]:
        query=self.session.query(WishlistORM)
        if ids:
            query=query.filter(WishlistORM.id.in_(ids))
        wishlists_orm= query.all()
        wishlists=[]
        for wishlist_orm in wishlists_orm:
            products = [
                Product(id=p.product.id, name=p.product.name, quantity=p.product.quantity, price=p.product.price)
                for p in wishlist_orm.products
            ]
            wishlists.append(Wishlist(id=wishlist_orm.id, customer=Customer(id=wishlist_orm.customer.id, name=wishlist_orm.customer.name), products=products))
        return wishlists
    
    def update(self, wishlist_id: int, wishlist: Wishlist):
        wishlist_orm= self.session.query(WishlistORM).filter_by(id=wishlist_id).one()
        wishlist_orm.customer = self.session.query(CustomerORM).filter_by(id=wishlist.customer.id).one()
        product_orms = [
            self.session.query(ProductORM).filter_by(id=p.id).one() for p in wishlist.products
        ]
        wishlist_orm.products = [
            WishlistProductORM(product=i, wishlist_id=wishlist_orm.id) for i in product_orms
        ]
        self.session.add(wishlist_orm)
        return self.get(wishlist_id)
    
    def delete(self, wishlist_id: int):
        wishlist_orm= self.session.query(WishlistORM).filter_by(id=wishlist_id).one()
        self.session.delete(wishlist_orm)