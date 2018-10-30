class Cart:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.product_id = kwargs.get("product_id")
        self.product_name = kwargs.get("product_name")
        self.quantity = kwargs.get("quantity")
        self.price = kwargs.get("price")

    def __repr__(self):
        return "<Cart(id={}, product_id={}, product_name={}, quantity={}, price={})>".format(
            self.id,
            self.product_id,
            self.product_name,
            self.quantity,
            self.price
        )


class Category:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.category_name = kwargs.get("category_name")
        self.price = kwargs.get("price")
        self.created_at = kwargs.get("created_at")
        self.modified_at = kwargs.get("modified_at")

    def __repr__(self):
        return "<Category(id={}, category_name={}, price={}, created_at={}, modified_at={})>".format(
            self.id,
            self.category_name,
            self.price,
            self.created_at,
            self.modified_at
        )


class Inventory:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.product_id = kwargs.get("product_id")
        self.quantity = kwargs.get("quantity")
        self.stock_level = kwargs.get("stock_level")
        self.min_quantity = kwargs.get("min_quantity")
        self.created_at = kwargs.get("created_at")
        self.modified_at = kwargs.get("modified_at")

    def __repr__(self):
        return "<Sale(id={}, product_id={}, quantity={}, stock_level={}, min_quantity={}, created_at={}, modified_at={})>".format(
            self.id,
            self.product_id,
            self.quantity,
            self.stock_level,
            self.min_quantity,
            self.created_at,
            self.modified_at
        )


class LineItem:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.product_id = kwargs.get("product_id")
        self.sales_id = kwargs.get("sales_id")
        self.product_name = kwargs.get("product_name")
        self.quantity = kwargs.get("quantity")
        self.price = kwargs.get("price")

    def __repr__(self):
        return "<LineItem(id={}, product_id={}, sales_id={}, product_name={}, quantity={}, price={})>".format(
            self.id,
            self.product_id,
            self.sales_id,
            self.product_name,
            self.quantity,
            self.price
        )


class Product:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.category_id = kwargs.get("category_id")
        self.product_name = kwargs.get('product_name')
        self.created_at = kwargs.get("created_at")
        self.modified_at = kwargs.get("modified_at")
        self.status = "Active"

    def __repr__(self):
        return "<Product(id={}, category_id={}, product_name={}, created_at={}, modified_at={})>".format(
            self.id,
            self.category_id,
            self.product_name,
            self.created_at,
            self.modified_at
        )


class SalesOrder:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.user_id = kwargs.get("user_id")
        self.order_number = kwargs.get("order_number")
        self.created_at = kwargs.get("created_at")
        self.modified_at = kwargs.get("modified_at")

    def __repr__(self):
        return "<SalesOrder(id={}, user_id={}, order_number={}, created_at={}, modified_at={})>".format(
            self.id,
            self.user_id,
            self.order_number,
            self.created_at,
            self.modified_at
        )


class User:

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.fullname = kwargs.get("fullname")
        self.username = kwargs.get("username")
        self.password = kwargs.get("password")
        self.roles = kwargs.get("roles")
        self.created_at = kwargs.get("created_at")
        self.modified_at = kwargs.get("modified_at")

    def __repr__(self):
        return "<User(id={}, name={}, username={}, roles={}, created_at={}, modified_at={})>".format(self.id, self.fullname, self.username, self.roles, self.created_at, self.modified_at)
