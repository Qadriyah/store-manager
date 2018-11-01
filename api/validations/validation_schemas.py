product_schema = {
    'category_id': {'type': 'integer', 'forbidden': ["", " "], 'required': True},
    'product_name': {'type': 'string', 'forbidden': ["", " "], 'required': True},
    'product_price': {'type': 'integer', 'forbidden': ["", " "], 'required': True}
}

category_schema = {
    'category_name': {'type': 'string', 'forbidden': ["", " "], 'required': True}
}

stock_schema = {
    'product_id': {'type': 'integer', 'forbidden': ["", " "], 'required': True},
    'quantity': {'type': 'integer', 'forbidden': ["", " "], 'required': True}
}

cart_schema = {
    'product_id': {'type': 'integer', 'forbidden': ["", " "], 'required': True},
    'quantity': {'type': 'integer', 'forbidden': ["", " "], 'required': True}
}

sales_schema = {
    'sales_date': {'type': 'string', 'forbidden': ["", " "], 'required': True}
}

register_schema = {
    'fullname': {'type': 'string', 'forbidden': ["", " "], 'required': True},
    'username': {'type': 'string', 'forbidden': ["", " "], 'required': True},
    'password': {'type': 'string', 'forbidden': ["", " "], 'required': True},
    'password2': {'type': 'string', 'forbidden': ["", " "], 'required': True},
    'roles': {'type': 'string', 'forbidden': ["", " "], 'required': True}
}

login_schema = {
    'username': {'type': 'string', 'forbidden': ["", " "], 'required': True},
    'password': {'type': 'string', 'forbidden': ["", " "], 'required': True}
}
