import pytest

from main import calculate_order_total


class TestCalculateTotalWithDiscount:
    def test_single_item_with_discount(self, single_item):
        result = calculate_order_total(single_item, apply_discount=True)
        assert result == 45.0

    def test_multiple_items_with_discount(self, multiple_items):
        result = calculate_order_total(multiple_items, apply_discount=True)
        assert result == 90.0
