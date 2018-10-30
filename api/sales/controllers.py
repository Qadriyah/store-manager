import secrets
from flask import jsonify
from flask_jwt_extended import current_user

from api import app
from models.models import SalesOrder, Cart


class SalesController:

    def __init__(self):
        self.status_code = 200

    ''' def add_to_cart(self, request_data):
        """
        Add products to the shopping cart

        Args:
            request_data(object): Object holding form data

        Returns:
            str: Message
        """
        response = {}
        if self.is_product_out_of_stock(request_data["pid"]):
            return jsonify({"msg": "Item is out of stock"}), 401

        if self.is_product_in_cart(request_data["name"]):
            self.update_qty_in_cart(request_data["pid"], request_data["qty"])
            response.update({"msg": "Success"})
            self.status_code = 200
        else:
            new_cart_item = Cart(
                pid=request_data["pid"],
                name=request_data["name"],
                qty=request_data["qty"],
                price=request_data["price"])
            cart.append(new_cart_item)
            response.update({"msg": "Success"})
            self.status_code = 200

        return jsonify(response), 200

    def get_cart_items(self):
        """
        Retrieves a list of all products from in the cart

        Returns:
            list: A list of products
        """
        response = {}
        if self.is_table_empty(cart):
            response.update({"msg": "Empty cart"})
            self.status_code = 404
        else:
            items = [
                dict(
                    id=product.product_id,
                    name=product.product_name,
                    qty=product.quantity,
                    price=product.price,
                    total=int(product.quantity) * int(product.price))
                for product in cart
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
        if self.is_table_empty(cart):
            response.update({"cart": "Empty cart"})
            self.status_code = 404
            return jsonify(response), self.status_code

        order_number = secrets.token_hex(8)
        user_id = 2
        if current_user:
            user_id = current_user.id

        for product in cart:
            new_sale = SalesOrder(
                id=product.product_id,
                user_id=user_id,
                order_number=order_number,
                created_at=""
            )
            sales_records.append(new_sale)
            #  Reduce stock
            self.reduce_stock(product.product_id, product.qty)
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
        if self.is_table_empty(cart):
            return found

        for product in cart:
            if product.product_name == product_name:
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
        for product in cart:
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
        cart.clear()

    def get_all_sales_records(self):
        """
        Retrieves all sales records from the database

        Returns:
            tuple: With all sales records and a status code
        """
        response = {}
        if self.is_table_empty(sales_records):
            response.update({"sales": "No sales"})
            self.status_code = 404
        else:
            items = [
                dict(
                    id=sales_item.id,
                    user_id=sales_item.user_id,
                    order_number=sales_item.order_number,
                    created_at=sales_item.created_at)
                for sales_item in sales_records
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
        for sales_item in sales_records:
            if sales_item.id == sales_id:
                response.update({
                    "id": sales_item.id,
                    "user_id": sales_item.user_id,
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

    def reduce_stock(self, product_id, quantity):
        """
        Reduces product quantity

        Args:
            product_id(str): Unique product identifier
            quantity(int): Quantity sold

        Returns:
            int: 1
        """
        for product in product_list:
            if product.id == product_id:
                temp = int(product.quantity)
                temp -= int(quantity)
                product.quantity = temp
                break
        return 1

    def is_product_out_of_stock(self, product_id):
        """
        Checks if an item is out of stock

        Args:
            product_id(str): Unique product identifier

        Returns:
            bool: True for out of stock, False otherwise
        """
        out_of_stock = False
        for product in product_list:
            if product.id == product_id and product.quantity <= 0:
                out_of_stock = True
                break
        return out_of_stock

    def generate_order_number(self, value):
        """
        Generates the order number with leading zeros

        Args:
            value(int): Sales order ID

        Returns:
            str: Representation of the order number
        """
        response = "0" * (5 - len(str(value)))
        response = "SO-{}{}".format(response, str(value))
        return response
 '''
