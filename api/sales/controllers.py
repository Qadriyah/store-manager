from flask import jsonify
from flask_jwt_extended import current_user

from api import app, connection
from models.models import SalesOrder, Cart


class SalesController:

    def __init__(self):
        self.status_code = 200
        self.cursor = connection.cursor

    def add_to_cart(self, data):
        """
        Add products to the shopping cart

        Args:
            request_data(object): Object holding form data

        Returns:
            str: Message
        """
        response = {}
        if self.is_product_out_of_stock(data.get("product_id"), data.get("quantity")):
            return jsonify({"msg": "Item is out of stock"}), 401

        if connection.is_item_exist("cart", data.get("product_name"), "product_name"):
            self.update_qty_in_cart(
                data.get("product_id"), data.get("quantity"))
            self.reduce_stock(data.get("product_id"), data.get("quantity"))
            return self.get_cart_items()
        else:
            try:
                query = """
                INSERT INTO cart(product_id, product_name, quantity, price) \
                VALUES({}, '{}', {}, {})
                """.format(
                    data.get("product_id"),
                    data.get("product_name"),
                    data.get("quantity"),
                    data.get("price")
                )
                self.cursor.execute(query)
                self.reduce_stock(data.get("product_id"), data.get("quantity"))
                response = self.get_cart_items()
                self.status_code = 200
            except Exception:
                response.update({"msg": "Database error"})
                self.status_code = 500

        return jsonify(response), self.status_code

    def is_product_out_of_stock(self, product_id, quantity):
        """
        Checks if an item is out of stock

        Args:
            product_id(str): Unique product identifier

        Returns:

        """
        out_of_stock = False
        try:
            query = """
            SELECT stock_level FROM inventory WHERE product_id = {} AND stock_level >= {} 
            """.format(product_id, quantity)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if not result:
                out_of_stock = True

        except Exception:
            return out_of_stock
        return out_of_stock

    def update_qty_in_cart(self, product_id, quantity):
        """
        Updates quantity if product is already in the cart

        Args:
            product_id(str): Product identifier
            qty(int): Product quantity
        """
        try:
            query = """
            UPDATE cart SET quantity = quantity + {} WHERE product_id = {}
            """.format(quantity, product_id)
            self.cursor.execute(query)
        except Exception:
            print("Database error")

    def reduce_stock(self, product_id, quantity):
        """
        Reduces product quantity

        Args:
            product_id(str): Unique product identifier
            quantity(int): Quantity sold
        """
        try:
            query = """
            UPDATE inventory SET stock_level = stock_level - {} WHERE product_id = {}
            """.format(
                quantity,
                product_id
            )
            self.cursor.execute(query)
        except Exception:
            print("Database error")

    def get_cart_items(self):
        """
        Retrieves a list of all products from in the cart

        Returns:
            list: A list of products
        """
        response = {}
        if not connection.is_table_empty("cart"):
            response.update({"msg": "Empty cart"})
            self.status_code = 404
        else:
            try:
                query = """
                SELECT \
                id, \
                product_name, \
                quantity, \
                price, \
                (quantity * price) AS total FROM cart
                """
                self.cursor.execute(query)
                response = self.cursor.fetchall()
                self.status_code = 200
            except Exception:
                print("Database error")

        return jsonify(response), self.status_code

    ''' 

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
