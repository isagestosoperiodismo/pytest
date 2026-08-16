import pytest

from main import calculate_order_total


class TestRaiseItemValidationErrors:
    @pytest.mark.parametrize(
        "items, expected_message",
        [
            ([{"quantity": 1}], "Each item must have 'price' and 'quantity'"),
            ([{"price": 50.0}], "Each item must have 'price' and 'quantity'"),
            ([{"price": 0, "quantity": 1}], "Price and quantity must be greater than 0"),
            ([{"price": 50.0, "quantity": 0}], "Price and quantity must be greater than 0"),
            ([{"price": -10.0, "quantity": 1}], "Price and quantity must be greater than 0"),
            ([{"price": 50.0, "quantity": -1}], "Price and quantity must be greater than 0")
        ]
    )
    def test_raise_item_validation_error(self, items, expected_message):
        with pytest.raises(ValueError, match=expected_message):
            calculate_order_total(items)