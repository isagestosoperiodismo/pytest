import pytest

from main import calculate_order_total


class TestRoundingBehavior:
    def test_rounding_to_two_decimals_without_discount(self):
        items = [{"price": 10.0, "quantity": 3}]  # 30.0
        result = calculate_order_total(items, apply_discount=False)
        assert result == 30.0
        assert isinstance(result, float)

    def test_rounding_to_two_decimals_with_discount(self):
        items = [{"price": 33.33, "quantity": 3}]  # 99.99, with discount: 89.991 -> 89.99
        result = calculate_order_total(items, apply_discount=True)
        assert result == 89.99
        assert isinstance(result, float)

    def test_rounding_multiple_items_with_discount(self):
        items = [
            {"price": 10.01, "quantity": 2},  # 20.02
            {"price": 5.99, "quantity": 1}    # 5.99
        ]
        # Total: 26.01, with 10% discount: 23.409 -> 23.41
        result = calculate_order_total(items, apply_discount=True)
        assert result == 23.41
