from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ProductORM(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name=Column(String)
    quantity=Column(Integer)
    price=Column(Float)

class CustomerORM(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    name=Column(String)

class WishlistORM(Base):
    __tablename__ = 'wishlists'
    id = Column(Integer, primary_key=True)
    customer_id=Column(Integer, ForeignKey('customers.id'))
    customer=relationship("CustomerORM")

class OrderORM(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    customer_id=Column(Integer, ForeignKey('customers.id'))
    customer=relationship("CustomerORM")


order_product_associations = Table(
    'order_product_associations', Base.metadata,
    Column('order_id', ForeignKey('orders.id')),
    Column('product_id', ForeignKey('products.id'))
)

OrderORM.products = relationship("ProductORM", secondary=order_product_associations)

wishlist_product_associations = Table(
    'wishlist_product_associations', Base.metadata,
    Column('wishlist_id', ForeignKey('wishlists.id')),
    Column('product_id', ForeignKey('products.id'))
)

WishlistORM.products = relationship("ProductORM", secondary=wishlist_product_associations)