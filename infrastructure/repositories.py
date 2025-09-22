from typing import List
from sqlalchemy.orm import Session
from domain.models import Order, Product, Customer, Wishlist
from domain.repositories import (
    ProductRepository,
    OrderRepository,
    CustomerRepository,
    WishlistRepository,
)
from .orm import (
    ProductORM,
    OrderORM,
    CustomerORM,
    WishlistORM,
    WishlistProductORM,
    OrderProductORM,
)


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, entity: Product):
        product_orm = ProductORM(
            name=entity.name,
            quantity=entity.quantity,
            price=entity.price,
        )
        self.session.add(product_orm)

    def get(self, id_: int) -> Product:
        product_orm = self.session.query(ProductORM).filter_by(id_=id_).one()
        return Product(
            id_=product_orm.id_,
            name=product_orm.name,
            quantity=product_orm.quantity,
            price=product_orm.price,
        )

    def list(self, ids: List[int] | None = None) -> List[Product]:
        query = self.session.query(ProductORM)
        if ids:
            query = query.filter(ProductORM.id_.in_(ids))
        products_orm = query.all()
        return [
            Product(id_=p.id_, name=p.name, quantity=p.quantity, price=p.price)
            for p in products_orm
        ]

    def update(self, id_: int, entity: Product):
        product_orm = self.session.query(ProductORM).filter_by(id_=id_).one()
        product_orm.name = entity.name
        product_orm.quantity = entity.quantity
        product_orm.price = entity.price
        self.session.add(product_orm)
        return self.get(id_)

    def delete(self, id_: int):
        product_orm = self.session.query(ProductORM).filter_by(id_=id_).one()
        self.session.delete(product_orm)


class SqlAlchemyCustomerRepository(CustomerRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, entity: Customer):
        customer_orm = CustomerORM(name=entity.name)
        self.session.add(customer_orm)

    def get(self, id_: int) -> Customer:
        customer_orm = self.session.query(CustomerORM).filter_by(id_=id_).one()
        return Customer(id_=customer_orm.id_, name=customer_orm.name)

    def list(self, ids: List[int] | None = None) -> List[Customer]:
        query = self.session.query(CustomerORM)
        if ids:
            query = query.filter(CustomerORM.id_.in_(ids))
        customers_orm = query.all()
        return [Customer(id_=c.id_, name=c.name) for c in customers_orm]

    def update(self, id_: int, entity: Customer):
        customer_orm = self.session.query(CustomerORM).filter_by(id_=id_).one()
        customer_orm.name = entity.name
        self.session.add(customer_orm)
        return self.get(id_)

    def delete(self, id_: int):
        customer_orm = self.session.query(CustomerORM).filter_by(id_=id_).one()
        self.session.delete(customer_orm)


class SqlAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, entity: Order):
        order_orm = OrderORM(
            customer_id=entity.customer.id_,
        )
        order_orm.customer = (
            self.session.query(CustomerORM).filter_by(id_=entity.customer.id_).one()
        )

        product_orms = [
            self.session.query(ProductORM).filter_by(id_=p.id_).one()
            for p in entity.products
        ]
        order_orm.products = [
            OrderProductORM(product=product_orms[i], order_id=order_orm.id_)
            for i in range(len(product_orms))
        ]
        self.session.add(order_orm)

    def get(self, id_: int) -> Order:
        order_orm = self.session.query(OrderORM).filter_by(id_=id_).one()
        products = [
            Product(
                id_=p.product.id_,
                name=p.product.name,
                quantity=p.product.quantity,
                price=p.product.price,
            )
            for p in order_orm.products
        ]
        return Order(
            id_=order_orm.id_,
            customer=Customer(id_=order_orm.customer.id_, name=order_orm.customer.name),
            products=products,
        )

    def list(self, ids: List[int] | None = None) -> List[Order]:
        query = self.session.query(OrderORM)
        if ids:
            query = query.filter(OrderORM.id_.in_(ids))
        orders_orm = query.all()
        orders = []
        for order_orm in orders_orm:
            products = [
                Product(
                    id_=p.product.id_,
                    name=p.product.name,
                    quantity=p.product.quantity,
                    price=p.product.price,
                )
                for p in order_orm.products
            ]
            orders.append(
                Order(
                    id_=order_orm.id_,
                    customer=Customer(
                        id_=order_orm.customer.id_, name=order_orm.customer.name
                    ),
                    products=products,
                )
            )
        return orders

    def update(self, id_: int, entity: Order):
        order_orm = self.session.query(OrderORM).filter_by(id_=id_).one()
        product_orms = [
            self.session.query(ProductORM).filter_by(id_=p.id_).one()
            for p in entity.products
        ]
        order_orm.products = [
            OrderProductORM(product=i, order_id=order_orm.id_) for i in product_orms
        ]
        self.session.add(order_orm)
        return self.get(id_)

    def delete(self, id_: int):
        order_orm = self.session.query(OrderORM).filter_by(id_=id_).one()
        self.session.delete(order_orm)


class SqlAlchemyWishlistRepository(WishlistRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, entity: Wishlist):
        wishlist_orm = WishlistORM()
        wishlist_orm.customer = (
            self.session.query(CustomerORM).filter_by(id_=entity.customer.id_).one()
        )
        product_orms = [
            self.session.query(ProductORM).filter_by(id_=p.id_).one()
            for p in entity.products
        ]
        wishlist_orm.products = [
            WishlistProductORM(product=i, wishlist_id=wishlist_orm.id_)
            for i in product_orms
            for p in entity.products
        ]
        self.session.add(wishlist_orm)

    def get(self, id_: int) -> Wishlist:
        wishlist_orm = self.session.query(WishlistORM).filter_by(id_=id_).one()
        products = [
            Product(
                id_=p.product.id_,
                name=p.product.name,
                quantity=p.product.quantity,
                price=p.product.price,
            )
            for p in wishlist_orm.products
        ]
        return Wishlist(
            id_=wishlist_orm.id_,
            customer=Customer(
                id_=wishlist_orm.customer.id_, name=wishlist_orm.customer.name
            ),
            products=products,
        )

    def list(self, ids: List[int] | None = None) -> List[Wishlist]:
        query = self.session.query(WishlistORM)
        if ids:
            query = query.filter(WishlistORM.id_.in_(ids))
        wishlists_orm = query.all()
        wishlists = []
        for wishlist_orm in wishlists_orm:
            products = [
                Product(
                    id_=p.product.id_,
                    name=p.product.name,
                    quantity=p.product.quantity,
                    price=p.product.price,
                )
                for p in wishlist_orm.products
            ]
            wishlists.append(
                Wishlist(
                    id_=wishlist_orm.id_,
                    customer=Customer(
                        id_=wishlist_orm.customer.id_, name=wishlist_orm.customer.name
                    ),
                    products=products,
                )
            )
        return wishlists

    def update(self, id_: int, entity: Wishlist):
        wishlist_orm = self.session.query(WishlistORM).filter_by(id_=id_).one()
        wishlist_orm.customer = (
            self.session.query(CustomerORM).filter_by(id_=entity.customer.id_).one()
        )
        product_orms = [
            self.session.query(ProductORM).filter_by(id_=p.id_).one()
            for p in entity.products
        ]
        wishlist_orm.products = [
            WishlistProductORM(product=i, wishlist_id=wishlist_orm.id_)
            for i in product_orms
        ]
        self.session.add(wishlist_orm)
        return self.get(id_)

    def delete(self, id_: int):
        wishlist_orm = self.session.query(WishlistORM).filter_by(id_=id_).one()
        self.session.delete(wishlist_orm)
