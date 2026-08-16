import pytest

from main import calculate_order_total  # Assuming the function is defined in main.py


class TestEmptyList:
    def test_empty_list_raise_error(self):
        with pytest.raises(ValueError, match="Items list cannot be empty"):
            calculate_order_total([])  # Assuming calculate_order_total is the function being tested
    
    def test_none_raise_error(self):
        with pytest.raises(ValueError, match="Items list cannot be empty"):
            calculate_order_total(None)  # Assuming calculate_order_total is the function being tested