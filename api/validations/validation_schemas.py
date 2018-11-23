product_schema = {
    'category_id': {'type': 'integer', 'forbidden': ["", " "], 'min': 1, 'required': True},
    'product_name': {'type': 'string', 'forbidden': ["", " "], 'required': True},
    'product_price': {'type': 'integer', 'forbidden': ["", " "], 'min': 1, 'required': True}
}

category_schema = {
    'category_name': {'type': 'string', 'forbidden': ["", " "], 'required': True}
}

stock_schema = {
    'product_id': {'type': 'integer', 'forbidden': ["", " "], 'min': 1, 'required': True},
    'quantity': {'type': 'integer', 'forbidden': ["", " "], 'min': 1, 'required': True}
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

date_schema = {
    'fro': {'type': 'string', 'forbidden': ["", " "], 'required': True},
    'to': {'type': 'string', 'forbidden': ["", " "], 'required': True},
    'user_id': {'type': 'integer', 'forbidden': ["", " "], 'min': 0, 'required': True}
}

update_user_schema = {
    'fullname': {'type': 'string', 'forbidden': ["", " "], 'required': True},
    'username': {'type': 'string', 'forbidden': ["", " "], 'required': True},
    'roles': {'type': 'string', 'forbidden': ["", " "], 'required': True}
}
