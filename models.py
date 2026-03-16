def ValidateProduct(product):
    """
    Validate product data
    """
    required_fields = ['name', 'category', 'quantity', 'price']
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in product:
            return False
    
    # Validate data types
    if not isinstance(product['name'], str) or len(product['name'].strip()) == 0:
        return False
    
    if not isinstance(product['category'], str) or len(product['category'].strip()) == 0:
        return False
    
    if not isinstance(product['quantity'], int) or product['quantity'] < 0:
        return False
    
    if not isinstance(product['price'], (int, float)) or product['price'] < 0:
        return False
    
    return True

def ValidateOrder(order):
    """
    Validate order data
    """
    required_fields = ['product_id', 'quantity']
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in order:
            return False
    
    # Validate data types
    if not isinstance(order['product_id'], int) or order['product_id'] <= 0:
        return False
    
    if not isinstance(order['quantity'], int) or order['quantity'] <= 0:
        return False
    
    return True

def ValidateTransaction(transaction):
    """
    Validate transaction data
    """
    required_fields = ['type', 'product_id', 'quantity']
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in transaction:
            return False
    
    # Validate data types
    if not isinstance(transaction['type'], str) or transaction['type'].strip() == '':
        return False
    
    valid_types = ['sale', 'return', 'transfer']
    if transaction['type'] not in valid_types:
        return False
    
    if not isinstance(transaction['product_id'], int) or transaction['product_id'] <= 0:
        return False
    
    if not isinstance(transaction['quantity'], int) or transaction['quantity'] <= 0:
        return False
    
    return True
