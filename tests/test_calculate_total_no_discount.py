import pytest

from main import calculate_order_total


class TestCalculateTotalNoDiscount:
    def test_single_item_no_discount(self, single_item):
        result = calculate_order_total(single_item, apply_discount=False)
        assert result == 50.0

    def test_multiple_items_no_discount(self, multiple_items):
        result = calculate_order_total(multiple_items, apply_discount=False)
        assert result == 100.0
