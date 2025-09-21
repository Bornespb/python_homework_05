from domain.unit_of_work import UnitOfWork
from infrastructure.repositories import SqlAlchemyProductRepository, SqlAlchemyOrderRepository, SqlAlchemyCustomerRepository, SqlAlchemyWishlistRepository
from sqlalchemy.orm import Session

class SqlAlchemyUnitOfWork(UnitOfWork):

    def __init__(self, session: Session):
        super().__init__(
            SqlAlchemyProductRepository(session),
            SqlAlchemyOrderRepository(session),
            SqlAlchemyCustomerRepository(session),
            SqlAlchemyWishlistRepository(session))
        self.session=session

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        if exception_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
