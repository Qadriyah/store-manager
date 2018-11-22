from flask import jsonify
from flask_jwt_extended import current_user

from api import connection, insert, select, update, delete


class SalesController:

    def __init__(self):
        self.status_code = 200
        self.cursor = connection.cursor

    def add_to_cart(self, data):
        """
        Add products to the shopping cart
        """
        response = {}
        if not self.check_negative_quantity(data.get("quantity")):
            return jsonify({"msg": "Quantity should be greater than zero"}), 401

        product = select.select_single_stock_level(data.get("product_id"))
        if product.get("msg") == "Empty":
            return jsonify({"msg": "Product does not exist"}), 404

        if product.get("stock").get("stock_level") < data.get("quantity"):
            return jsonify({"msg": "Product is out of stock"}), 401

        data.update({
            "user_id": current_user.id,
            "product_name": product.get("stock").get("product_name"),
            "product_price": product.get("stock").get("product_price")
        })
        if connection.is_item_exist("product_id", "cart", data.get("product_id")):
            update.update_qty_in_cart(
                data.get("product_id"), data.get("quantity"))
        else:
            insert.insert_cart(data)

        update.update_stock_level(
            data.get("product_id"), data.get("quantity"), "add")
        cart = select.select_cart_items(current_user.id)
        response.update({"cart": cart.get("cart")})
        self.status_code = 200

        return jsonify(response), self.status_code

    def check_negative_quantity(self, quantity):
        if quantity <= 0:
            return False
        return True

    def get_cart_items(self):
        """
        Retrieves a list of all products from in the cart

        Returns:
            list: A list of products
        """
        response = {}
        items = select.select_cart_items(current_user.id)
        if items.get("msg") == "Empty":
            response.update({"msg": "No items in the shopping cart"})
            self.status_code = 404
        else:
            response.update({"cart": items.get("cart")})
            self.status_code = 200

        return jsonify(response), self.status_code

    def delete_cart_item(self, cart_id):
        response = {}
        result = select.select_single_cart_item(cart_id)
        if result.get("msg") == "Empty":
            return jsonify({"msg": "Cart item not found"}), 404

        deleted = delete.delete_from_table("cart", cart_id)
        if deleted.get("msg") == "Success":
            update.update_stock_level(result.get("cart").get(
                "product_id"), result.get("cart").get("quantity"), "del")

            cart = select.select_cart_items(current_user.id)
            response.update({
                "cart": cart.get("cart"),
                "msg": "Item deleted successfully"
            })
            self.status_code = 200
        else:
            response.update({"msg": "Server error"})
            self.status_code = 500

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
        cart_items = select.select_cart_items(current_user.id)
        if cart_items.get("msg") == "Empty":
            response.update({"msg": "Empty cart"})
            self.status_code = 404
        else:
            cart_items.update({"user_id": current_user.id})
            response = insert.insert_salesorder(cart_items)
            if response.get("msg") == "Success":
                connection.clear_table("cart")
                self.status_code = 200
            else:
                self.status_code = 500

        return jsonify(response), self.status_code

    def get_all_sales_records(self, data, option):
        """
        Retrieves all sales records from the database

        Returns:
            tuple: With all sales records and a status code
        """
        response = {}
        query = """
        SELECT id, user_id, created_at FROM salesorder WHERE created_at \
        BETWEEN '{}'::DATE AND '{}'::DATE  ORDER BY created_at DESC
        """.format(data.get('fro'), data.get('to'))

        if option == "single":
            query = """
            SELECT id, user_id, created_at FROM salesorder WHERE id = {}
            """.format(data.get('sales_id'))

        if option == "user" or data.get("user_id") > 0:
            query = """
            SELECT id, user_id, created_at FROM salesorder WHERE user_id = {} \
            AND created_at BETWEEN '{}'::DATE AND '{}'::DATE ORDER BY created_at DESC
            """.format(data.get('user_id'), data.get('fro'), data.get('to'))

        response = select.select_sales_records(query)
        if response.get("msg") == "Empty":
            return jsonify({"msg": "No sales found"}), 404

        if response.get("msg") == "Success":
            self.status_code = 200
        else:
            self.status_code = 500

        return jsonify(response), self.status_code
