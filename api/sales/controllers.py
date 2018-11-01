from flask import jsonify, json
from flask_jwt_extended import current_user

from api import app, connection
from api.product.controllers import ProductController

pcontroller = ProductController()


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

        res = pcontroller.get_single_product(data.get("product_id"))
        product = json.loads(res[0].data)
        if connection.is_item_exist("cart", product.get("product_name"), "product_name"):
            self.update_qty_in_cart(
                data.get("product_id"), data.get("quantity"))
            self.modify_stock(data.get("product_id"),
                              data.get("quantity"), "reduce")
            return self.get_cart_items()
        else:
            try:
                query = """
                INSERT INTO cart(product_id, product_name, quantity, price) \
                VALUES({}, '{}', {}, {})
                """.format(
                    data.get("product_id"),
                    product.get("product_name"),
                    data.get("quantity"),
                    product.get("product_price")
                )
                self.cursor.execute(query)
                self.modify_stock(data.get("product_id"),
                                  data.get("quantity"), "reduce")
                response = json.loads(self.get_cart_items()[0].data)
                self.status_code = 200
            except Exception as error:
                response.update({"msg": "Database error {}".format(error)})
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

    def modify_stock(self, product_id, quantity, operation):
        """
        Reduces product quantity

        Args:
            product_id(str): Unique product identifier
            quantity(int): Quantity sold
        """
        try:
            query1 = """
            UPDATE inventory \
            SET stock_level = stock_level - {} WHERE product_id = {}
            """.format(
                quantity,
                product_id
            )
            query2 = """
            UPDATE inventory \
            SET stock_level = stock_level + {} WHERE product_id = {}
            """.format(
                quantity,
                product_id
            )
            if operation == "raise":
                self.cursor.execute(query2)
            if operation == "reduce":
                self.cursor.execute(query1)
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
                SELECT id, product_id, product_name, quantity, price, \
                (quantity * price) AS total FROM cart
                """
                self.cursor.execute(query)
                response = self.cursor.fetchall()
                self.status_code = 200
            except Exception:
                print("Database error")

        return jsonify(response), self.status_code

    def add_sales_record(self, cart_items):
        """
        Adds cart items into the sales record database

        Args:
            cart(object): Object that holds cart items

        Returns:
            tuple: With a response message and a status code
        """
        response = {}
        if not connection.is_table_empty("cart"):
            response.update({"msg": "Empty cart"})
            self.status_code = 404
        else:
            try:
                query = """
                INSERT INTO salesorder(user_id) \
                VALUES({}) RETURNING id
                """.format(current_user.id)
                self.cursor.execute(query)
                order_id = self.cursor.fetchone()
                for product in json.loads(cart_items.data):
                    self.add_line_items(
                        product.get("product_id"),
                        order_id.get("id"), product.get("product_name"),
                        product.get("quantity"), product.get("price"))
                connection.clear_table("cart")
                response.update({"msg": "Sales order submitted successfully"})
                self.status_code = 200
            except Exception as error:
                response.update({"msg": "Database error {}".format(error)})
                self.status_code = 500
        return jsonify(response), self.status_code

    def add_line_items(self, pid, sid, pname, qty, price):
        """
        Adds sales line items
        """
        try:
            query = """
            INSERT INTO line_items(product_id, sales_id, product_name, quantity, price) \
            VALUES({}, {}, '{}', {}, {})
            """.format(
                pid,
                sid,
                pname,
                qty,
                price
            )
            self.cursor.execute(query)
        except Exception as error:
            print("Database error {}".format(error))

    def delete_cart_item(self, cart_id, product_id, quantity):
        response = {}
        try:
            query = """
            DELETE FROM cart WHERE id = {}
            """.format(cart_id)
            self.cursor.execute(query)
            self.modify_stock(product_id, quantity, "raise")
            response.update({"msg": "Product deleted from cart"})
            self.status_code = 200
        except Exception:
            response.update({"msg": "Database error"})
            self.status_code = 505
        return jsonify(response), self.status_code

    def get_all_sales_records(self):
        """
        Retrieves all sales records from the database

        Returns:
            tuple: With all sales records and a status code
        """
        response = {}
        orders = []
        if not connection.is_table_empty("salesorder"):
            response.update({"sales": "No sales"})
            self.status_code = 404
        else:
            query = """
            SELECT * FROM salesorder ORDER BY created_at DESC
            """
            self.cursor.execute(query)
            sales_orders = self.cursor.fetchall()
            for item in sales_orders:
                temp = {}
                temp.update({
                    "order_number": self.generate_order_number(item.get("id")),
                    "order_date": item.get("created_at"),
                    "sold_by": self.get_user_details(item.get("user_id")).get("fullname"),
                    "items": self.get_line_items(item.get("id"))
                })
                orders.append(temp)
            response = {"orders": orders}
            self.status_code = 200

        return jsonify(response), self.status_code

    def get_line_items(self, sales_id):
        response = {}
        try:
            query = """
            SELECT *, (quantity * price) AS total FROM line_items \
            WHERE sales_id = {}
            """.format(sales_id)
            self.cursor.execute(query)
            response = self.cursor.fetchall()
        except Exception:
            print("Database error")
        return response

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

    def get_user_details(self, user_id):
        response = {}
        try:
            query = """
            SELECT id, fullname, username, roles FROM users WHERE id = {}
            """.format(user_id)
            self.cursor.execute(query)
            response = self.cursor.fetchone()
            if not response:
                response = {}
                response.update({"msg": "User not found"})
                self.status_code = 404
        except Exception:
            print("Database error")
        return response

    def get_single_sales_record(self, sales_id):
        """
        Retrieves a single sales records using the sales_id

        Args:
            sales_id(str): Sales record unique identifier

        Returns:
            tuple: With a single sales record and a status code
        """
        response = {}
        try:
            query = """
            SELECT * FROM salesorder WHERE id = {}
            """.format(sales_id)
            self.cursor.execute(query)
            sales_orders = self.cursor.fetchone()
            response.update({
                "order_number": self.generate_order_number(sales_orders.get("id")),
                "order_date": sales_orders.get("created_at"),
                "sold_by": self.get_user_details(sales_orders.get("user_id")).get("fullname"),
                "items": self.get_line_items(sales_orders.get("id"))
            })
            self.status_code = 200
            if not response:
                response.update({"msg": "Sales record not found"})
                self.status_code = 404
        except Exception as error:
            print("Database error {}".format(error))
        return jsonify(response), self.status_code

    def get_sales_for_attendant(self, user_id):
        """
        Retrieves all sales for a particular sales attendant
        """
        response = {}
        try:
            query = """
            SELECT * FROM salesorder WHERE user_id = {} ORDER BY created_at DESC
            """.format(user_id)
            self.cursor.execute(query)
            sales_orders = self.cursor.fetchall()
            for item in sales_orders:
                response.update({
                    "order_number": self.generate_order_number(item.get("id")),
                    "order_date": item.get("created_at"),
                    "sold_by": self.get_user_details(item.get("user_id")).get("fullname"),
                    "items": self.get_line_items(item.get("id"))
                })
            self.status_code = 200
            if not response:
                response.update({"msg": "Sales record not found"})
                self.status_code = 404
        except Exception:
            print("Database error")
        return jsonify(response), self.status_code
