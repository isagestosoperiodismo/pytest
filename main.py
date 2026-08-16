def calculate_order_total(items, apply_discount=False):
    """Calculates the total cost of an order with optional discount.
    
    Args:
        items (List): List of dictionaries with 'price' and 'quantity' keys
        apply_discount (bool): Whether to apply discount
        
    Returns:
        float: Total order amount
        
    Raises:
        ValueError: If items list is empty or items have invalid values
    """
    
    if not items:
        raise ValueError("Items list cannot be empty")
    
    subtotal = 0
    for item in items:
        if 'price' not in item or 'quantity' not in item:
            raise ValueError("Each item must have 'price' and 'quantity' keys")
        
        if item['price'] <= 0 or item['quantity'] <= 0:
            raise ValueError("Price and quantity must be greater than 0")
        
        subtotal += item['price'] * item['quantity']
    
    if apply_discount:
        discount = subtotal * 0.10
        total = subtotal - discount
    else:
        total = subtotal
    
    return round(total, 2)
