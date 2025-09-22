import pytest
from domain.models import Product, Order, Customer, Wishlist

@pytest.fixture
def two_same_products():
    return [Product(id_=1, name="product1", quantity=1, price=100),
    Product(id_=1, name="product1", quantity=1, price=100)]


@pytest.fixture
def two_different_products():
    return [Product(id_=1, name="product1", quantity=2, price=100),
    Product(id_=2, name="product2", quantity=3, price=200)]


def test_add_product_to_order_same_products(two_same_products):
    order = Order(id_=1, customer=Customer(id_=1, name="customer1"), products=[])
    [order.add_product(product) for product in two_same_products]
    assert len(order.products) == 1
    assert order.products[0].quantity == 2
    assert order.checkout() == 200


def test_add_product_to_order_different_products(two_different_products):
    order = Order(id_=1, customer=Customer(id_=1, name="customer1"), products=[])
    [order.add_product(product) for product in two_different_products]
    assert len(order.products) == 2
    assert order.products[0].quantity == 2
    assert order.products[1].quantity == 3
    assert order.checkout() == 800


def test_wishlist_add_product_same_products(two_same_products):
    wishlist = Wishlist(id_=1, customer=Customer(id_=1, name="customer1"), products=[])
    [wishlist.add_product(product) for product in two_same_products]
    assert len(wishlist.products) == 1
    assert wishlist.products[0].quantity == 2


def test_wishlist_add_product_different_products(two_different_products):
    wishlist = Wishlist(id_=1, customer=Customer(id_=1, name="customer1"), products=[])
    [wishlist.add_product(product) for product in two_different_products]
    assert len(wishlist.products) == 2
    assert wishlist.products[0].quantity == 2
    assert wishlist.products[1].quantity == 3
