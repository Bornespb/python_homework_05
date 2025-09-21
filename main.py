from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.services import OrderService, ProductService, CustomerService, WishlistService
from infrastructure.orm import Base
from infrastructure.repositories import SqlAlchemyProductRepository, SqlAlchemyOrderRepository, SqlAlchemyCustomerRepository, SqlAlchemyWishlistRepository
from infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from infrastructure.database import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionFactory=sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def main():
    uow = SqlAlchemyUnitOfWork(SessionFactory())

    product_service = ProductService(uow)
    order_service = OrderService(uow)
    customer_service = CustomerService(uow)
    wishlist_service = WishlistService(uow)

    with uow:
        new_product = product_service.create_product(id=1, name="product1", quantity=1, price=100)
        print(f"create product: {new_product}")
        new_customer = customer_service.create_customer(id=1, name="customer1")
        print(f"create customer: {new_customer}")
        new_wishlist = wishlist_service.create_wishlist(id=1, customer=new_customer)
        print(f"create wishlist: {new_wishlist}")
        new_wishlist = wishlist_service.add_product_to_wishlist(new_wishlist.id, new_product)
        print(f"create wishlist: {new_wishlist}")
        new_order = order_service.create_order(id=1, customer=new_customer, products=[new_product])
        new_order = order_service.add_product_to_order(new_order.id, new_product)
        new_order = order_service.checkout_order(new_order.id)
        print(f"create order: {new_order}")
        uow.commit()

if __name__ == "__main__":
    main()
