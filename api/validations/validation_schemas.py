product_schema = {
    'category_id': {'type': 'integer', 'required': True},
    'product_name': {'type': 'string', 'required': True}
}

category_schema = {
    'category_name': {'type': 'string', 'required': True},
    'price': {'type': 'integer', 'required': True},
    'created_at': {'type': 'string', 'required': True}
}

stock_schema = {
    'product_id': {'type': 'integer', 'required': True},
    'quantity': {'type': 'integer', 'required': True}
}

cart_schema = {
    'product_id': {'type': 'integer', 'required': True},
    'product_name': {'type': 'string', 'required': True},
    'quantity': {'type': 'integer', 'required': True},
    'price': {'type': 'integer', 'required': True}
}

sales_schema = {
    'sales_date': {'type': 'string', 'required': True}
}

register_schema = {
    'fullname': {'type': 'string', 'required': True},
    'username': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True},
    'password2': {'type': 'string', 'required': True},
    'roles': {'type': 'string', 'required': True}
}

login_schema = {
    'username': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True}
}
