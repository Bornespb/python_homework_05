from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from domain.services import OrderService, ProductService, CustomerService, WishlistService
from infrastructure.orm import Base
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
        new_product = product_service.create(id=1, name="product1", quantity=1, price=100)
        print(f"create product: {new_product}")
        new_customer = customer_service.create(id=1, name="customer1")
        print(f"create customer: {new_customer}")
        new_wishlist = wishlist_service.create(id=1, customer=new_customer)
        print(f"create wishlist: {new_wishlist}")
        new_wishlist = wishlist_service.add_product_to_wishlist(new_wishlist.id, new_product)
        print(f"create wishlist: {new_wishlist}")
        new_order = order_service.create(id=1, customer=new_customer, products=[new_product])
        print(f"create order: {new_order}")
        empty_order = order_service.create(id=2, customer=new_customer, products=[])
        print(f"create empty order: {empty_order}")
        updated_order = order_service.add_product_to_order(empty_order.id, new_product)
        print(f"add product to order: {updated_order}")
        checked_out_order = order_service.checkout_order(updated_order.id)
        print(f"checkout order: {checked_out_order}")
        uow.commit()

if __name__ == "__main__":
    main()
