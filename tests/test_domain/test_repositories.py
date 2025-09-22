import pytest
from abc import ABC
from domain.repositories import BaseRepository, ProductRepository, OrderRepository, CustomerRepository, WishlistRepository

function_names = ["add", "get", "list", "update", "delete"]

def test_base_repository_abstract():
    assert issubclass(BaseRepository, ABC)
    assert all(hasattr(BaseRepository, attr) for attr in function_names)


@pytest.mark.parametrize(
    "repository",
    [ProductRepository, OrderRepository, CustomerRepository, WishlistRepository]
)
def test_repositories_signature(repository):
    assert all(hasattr(repository, attr) for attr in function_names)
    assert issubclass(repository, BaseRepository)
    assert all(callable(getattr(repository, attr)) for attr in function_names)