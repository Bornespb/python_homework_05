import pytest
from unittest.mock import Mock, patch
from domain.services import BaseService, ProductService, OrderService, CustomerService, WishlistService
from domain.models import Product, Order, Customer, Wishlist
function_names = ["create", "get", "list", "update", "delete"]

@pytest.fixture(autouse=True)
def cleanup_patches():
    """Автоматически очищает все патчи после каждого теста"""
    yield
    patch.stopall()

@pytest.mark.parametrize(
    "service",
    [ProductService, OrderService, CustomerService, WishlistService]
)
def test_services_signature(service):
    assert all(hasattr(service, attr) for attr in function_names)
    assert issubclass(service, BaseService)
    assert all(callable(getattr(service, attr)) for attr in function_names)


@pytest.mark.parametrize(
    "service, repo_name, model, expected, kwargs",
    [
        (
            ProductService,
            "product_repo",
            Product,
            Product(id_=1, name="product1", quantity=1, price=100),
            {'id_':1, 'name':"product1", 'quantity':1, 'price':100}
        ),
        (
            OrderService,
            "order_repo",
            Order,
            Order(id_=1, customer=Customer(id_=1, name="customer1"), products=[Product(id_=1, name="product1", quantity=1, price=100)]),
            {'id_':1, 'customer':Customer(id_=1, name="customer1"), 'products':[Product(id_=1, name="product1", quantity=1, price=100)]}
        ),
        (
            CustomerService,
            "customer_repo",
            Customer,
            Customer(id_=1, name="customer1"),
            {'id_':1, 'name':"customer1"}
        ),
        (
            WishlistService,
            "wishlist_repo",
            Wishlist,
            Wishlist(id_=1, customer=Customer(id_=1, name="customer1")),
            {'id_':1, 'customer':Customer(id_=1, name="customer1"), 'products':[]}
        ),
    ]
)
def test_services_create(service, repo_name, model, expected, kwargs):
    mock_model = Mock()
    mock_add = Mock()
    mock_uow = Mock()
    setattr(model, "__new__", mock_model)
    setattr(mock_uow, repo_name, Mock())
    getattr(mock_uow, repo_name).add = mock_add
    mock_uow.commit = Mock()

    service = service(mock_uow)
    expected_object = expected
    mock_model.return_value = expected_object
        
    test_object = service.create(**kwargs)

    mock_model.assert_called_once_with(model, **kwargs)
    mock_add.assert_called_once_with(expected_object)
    mock_uow.commit.assert_called_once()
    assert test_object == expected_object


@pytest.mark.parametrize(
    "service, repo_name, expected, id_",
    [
        (
            ProductService,
            "product_repo",
            Product(id_=1, name="product1", quantity=1, price=100),
            1
        ),
        (
            OrderService,
            "order_repo",
            Order(id_=1, customer=Customer(id_=1, name="customer1"), products=[Product(id_=1, name="product1", quantity=1, price=100)]),
            1
        ),
        (
            CustomerService,
            "customer_repo",
            Customer(id_=1, name="customer1"),
            1
        ),
        (
            WishlistService,
            "wishlist_repo",
            Wishlist(id_=1, customer=Customer(id_=1, name="customer1")),
            1
        ),
    ]
)
def test_services_get(service, repo_name, expected, id_):
    mock_get = Mock()
    mock_uow = Mock()
    setattr(mock_uow, repo_name, Mock())
    getattr(mock_uow, repo_name).get = mock_get

    service = service(mock_uow)
    
    expected_object = expected
    mock_get.return_value = expected_object
      
    test_object = service.get(id_)

    mock_get.assert_called_once_with(id_)
    assert test_object == expected_object

@pytest.mark.parametrize(
    "service, repo_name, expected, ids",
    [
        (
            ProductService,
            "product_repo",
            [Product(id_=1, name="product1", quantity=1, price=100), Product(id_=2, name="product2", quantity=2, price=200)],
            [1]
        ),
        (
            OrderService,
            "order_repo",
            [Order(id_=1, customer=Customer(id_=1, name="customer1"), products=[Product(id_=1, name="product1", quantity=1, price=100)]),
             Order(id_=2, customer=Customer(id_=2, name="customer2"), products=[Product(id_=2, name="product2", quantity=2, price=200)])],
            [1, 2]
        ),
        (
            CustomerService,
            "customer_repo",
            [Customer(id_=1, name="customer1"), Customer(id_=2, name="customer2")],
            [1]
        ),
        (
            WishlistService,
            "wishlist_repo",
            [Wishlist(id_=1, customer=Customer(id_=1, name="customer1")), Wishlist(id_=2, customer=Customer(id_=2, name="customer2"))],
            [1, 2]
        ),
    ]
)
def test_services_list(service, repo_name, expected, ids):
    mock_list = Mock()
    mock_uow = Mock()
    setattr(mock_uow, repo_name, Mock())
    getattr(mock_uow, repo_name).list = mock_list

    service = service(mock_uow)
    mock_list.return_value = expected
    test_object = service.list(ids)
    mock_list.assert_called_once_with(ids)
    assert test_object == expected

@pytest.mark.parametrize(
    "service, repo_name, expected, id_",
    [
        (
            ProductService,
            "product_repo",
            Product(id_=1, name="product1", quantity=2, price=100),
            1
        ),
        (
            OrderService,
            "order_repo",
            Order(id_=1, customer=Customer(id_=1, name="customer1"), products=[Product(id_=1, name="product1", quantity=2, price=100)]),
            1
        ),
        (
            CustomerService,
            "customer_repo",
            Customer(id_=1, name="customer2"),
            1
        ),
        (
            WishlistService,
            "wishlist_repo",
            Wishlist(id_=1, customer=Customer(id_=1, name="customer2")),
            1
        ),
    ]
)
def test_services_update(service, repo_name, expected, id_):
    mock_update = Mock()
    mock_uow = Mock()
    setattr(mock_uow, repo_name, Mock())
    getattr(mock_uow, repo_name).update = mock_update

    service = service(mock_uow)
    mock_update.return_value = expected
    test_object = service.update(id_, expected)
    mock_update.assert_called_once_with(id_, expected)
    mock_uow.commit.assert_called_once()
    assert test_object == expected

@pytest.mark.parametrize(
    "service, repo_name, id_",
    [
        (
            ProductService,
            "product_repo",
            1
        ),
        (
            OrderService,
            "order_repo",
            1
        ),
        (
            CustomerService,
            "customer_repo",
            1
        ),
        (
            WishlistService,
            "wishlist_repo",
            1
        ),
    ]
)
def test_services_delete(service, repo_name, id_):
    mock_delete = Mock()
    mock_uow = Mock()
    setattr(mock_uow, repo_name, Mock())
    getattr(mock_uow, repo_name).delete = mock_delete

    service = service(mock_uow)
    service.delete(id_)
    mock_delete.assert_called_once_with(id_)
    mock_uow.commit.assert_called_once()
