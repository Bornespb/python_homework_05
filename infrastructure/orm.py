from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass


class ProductORM(Base):
    __tablename__ = "products"
    id_: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    quantity: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)


class CustomerORM(Base):
    __tablename__ = "customers"
    id_: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)


class OrderProductORM(Base):
    __tablename__ = "order_products"
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id_"), primary_key=True
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id_"), primary_key=True
    )
    product: Mapped[ProductORM] = relationship(lazy="joined")


class OrderORM(Base):
    __tablename__ = "orders"
    id_: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customers.id_"))
    customer: Mapped[CustomerORM] = relationship(lazy="joined")
    products: Mapped[list[OrderProductORM]] = relationship(
        cascade="all, delete-orphan", backref="orders"
    )


class WishlistProductORM(Base):
    __tablename__ = "wishlist_products"
    wishlist_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("wishlists.id_"), primary_key=True
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id_"), primary_key=True
    )
    product: Mapped[ProductORM] = relationship(lazy="joined")


class WishlistORM(Base):
    __tablename__ = "wishlists"
    id_: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("customers.id_"))
    customer: Mapped[CustomerORM] = relationship(lazy="joined")
    products: Mapped[list[WishlistProductORM]] = relationship(
        cascade="all, delete-orphan", backref="wishlists"
    )
