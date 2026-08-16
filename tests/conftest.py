import pytest


@pytest.fixture
def single_item():
    return [{'price': 50.0, 'quantity': 1}]


@pytest.fixture
def multiple_items():
    return [
        {'price': 50.0, 'quantity': 1},
        {'price': 25.0, 'quantity': 2}
    ]
