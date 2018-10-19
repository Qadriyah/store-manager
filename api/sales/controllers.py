import secrets
from flask import jsonify

from api import app
from api.models.sale import Sale
from api.models.cart import Cart


class SalesController:

    def __init__(self):
        self.status_code = 200
        self.sales_records = []
        self.cart = []

    def add_to_cart(self, request_data):
        """
        Add products to the shopping cart

        Args:
            request_data(object): Object holding form data

        Returns:
            str: Message
        """
        if self.is_product_in_cart(request_data["name"]):
            self.update_qty_in_cart(request_data["pid"], request_data["qty"])
        else:
            new_cart_item = Cart(
                pid=request_data["pid"],
                name=request_data["name"],
                qty=request_data["qty"],
                price=request_data["price"])
            self.cart.append(new_cart_item)

        return "Success"

    def get_cart_items(self):
        """
        Retrieves a list of all products from in the cart

        Returns:
            list: A list of products
        """
        response = {}
        if self.is_table_empty(self.cart):
            response.update({"msg": "Empty cart"})
            self.status_code = 404
        else:
            items = [
                dict(
                    id=product.product_id,
                    name=product.name,
                    qty=product.qty,
                    price=product.price,
                    total=int(product.qty) * int(product.price))
                for product in self.cart
            ]
            response.update({"items": items})
            self.status_code = 200
        return jsonify(response), self.status_code

    def add_sales_record(self):
        """
        Adds cart items into the sales record database

        Args:
            cart(object): Object that holds cart items

        Returns:
            tuple: With a response message and a status code
        """
        response = {}
        if self.is_table_empty(self.cart):
            response.update({"cart": "Empty cart"})
            self.status_code = 404
            return jsonify(response), self.status_code

        order_number = secrets.token_hex(8)
        for product in self.cart:
            new_sale = Sale(
                id=secrets.token_hex(4),
                user_id=1,
                order_number=order_number,
                product_id=product.product_id,
                qty=product.qty,
                price=product.price,
                product_name=product.name
            )
            self.sales_records.append(new_sale)
        #  clear the shopping cart
        self.clear_cart()

        response.update({"msg": "Sales order submitted successfully"})
        self.status_code = 200

        return jsonify(response), self.status_code

    def is_product_in_cart(self, product_name):
        """
        Checks if product has already been added to the cart

        Args:
            product_name(str): Product to check for

        Returns:
            bool: True if found, False otherwise
        """
        found = False
        if self.is_table_empty(self.cart):
            return found

        for product in self.cart:
            if product.name == product_name:
                found = True
                break
        return found

    def update_qty_in_cart(self, product_id, qty):
        """
        Updates quantity if product is already in the cart

        Args:
            product_id(str): Product identifier
            qty(int): Product quantity

        Returns:
            int: 1
        """
        for product in self.cart:
            if product.product_id == product_id:
                temp = int(product.qty)
                temp += int(qty)
                product.qty = str(temp)
                break
        return 1

    def is_table_empty(self, table):
        """
        Checks if a relation is empty

        Returns:
            bool: True if empty, False otherwise
        """
        if len(table) == 0:
            return True
        return False

    def clear_cart(self):
        """Removes items from the shopping cart"""
        self.cart.clear()

    def get_all_sales_records(self):
        """
        Retrieves all sales records from the database

        Returns:
            tuple: With all sales records and a status code
        """
        response = {}
        if self.is_table_empty(self.sales_records):
            response.update({"sales": "No sales"})
            self.status_code = 404
        else:
            items = [
                dict(
                    id=sales_item.id,
                    user_id=sales_item.user_id,
                    order_number=sales_item.order_number,
                    product_id=sales_item.product_id,
                    qty=sales_item.qty,
                    product_name=sales_item.product_name,
                    price=sales_item.price,
                    created_at=sales_item.created_at,
                    total=int(sales_item.price) * int(sales_item.qty))
                for sales_item in self.sales_records
            ]
            response.update({"items": items})
            self.status_code = 200

        return jsonify(response), self.status_code

    def get_single_sales_record(self, sales_id):
        """
        Retrieves a single sales records using the sales_id

        Args:
            sales_id(str): Sales record unique identifier

        Returns:
            tuple: With a single sales record and a status code
        """
        response = {}
        found = False
        for sales_item in self.sales_records:
            if sales_item.id == sales_id:
                response.update({
                    "id": sales_item.id,
                    "user_id": sales_item.user_id,
                    "name": sales_item.product_name,
                    "price": sales_item.price,
                    "qty": sales_item.qty,
                    "total": int(sales_item.price) * int(sales_item.qty),
                    "created_at": sales_item.created_at
                })
                found = True
                break
        if found:
            self.status_code = 200
            return jsonify(response), self.status_code

        response.update({"msg": "Sales record not found"})
        self.status_code = 404
        return jsonify(response), self.status_code
