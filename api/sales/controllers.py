from flask import jsonify
from flask_jwt_extended import current_user

from api import connection
from models.insert import Insert
from models.select import Select
from models.update import Update
from models.delete import Delete


class SalesController:

    def __init__(self):
        self.status_code = 200
        self.cursor = connection.cursor
        self.insert = Insert()
        self.select = Select()
        self.update = Update()
        self.delete = Delete()

    def add_to_cart(self, data):
        """
        Add products to the shopping cart
        """
        response = {}
        if not self.check_negative_quantity(data.get("quantity")):
            return jsonify({"msg": "Quantity should be greater than zero"}), 401

        product = self.select.select_single_stock_level(data.get("product_id"))
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
            self.update.update_qty_in_cart(
                data.get("product_id"), data.get("quantity"))
        else:
            self.insert.insert_cart(data)

        self.update.update_stock_level(
            data.get("product_id"), data.get("quantity"), "add")
        cart = self.select.select_cart_items(current_user.id)
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
        items = self.select.select_cart_items(current_user.id)
        if items.get("msg") == "Empty":
            response.update({"msg": "No items in the shopping cart"})
            self.status_code = 404
        else:
            response.update({"cart": items.get("cart")})
            self.status_code = 200

        return jsonify(response), self.status_code

    def delete_cart_item(self, cart_id):
        response = {}
        result = self.select.select_single_cart_item(cart_id)
        if result.get("msg") == "Empty":
            return jsonify({"msg": "Cart item not found"}), 404

        deleted = self.delete.delete_from_table("cart", cart_id)
        if deleted.get("msg") == "Success":
            self.update.update_stock_level(result.get("cart").get(
                "product_id"), result.get("cart").get("quantity"), "del")

            cart = self.select.select_cart_items(current_user.id)
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
        cart_items = self.select.select_cart_items(current_user.id)
        if cart_items.get("msg") == "Empty":
            response.update({"msg": "Empty cart"})
            self.status_code = 404
        else:
            cart_items.update({"user_id": current_user.id})
            response = self.insert.insert_salesorder(cart_items)
            if response.get("msg") == "Success":
                connection.clear_table("cart")
                self.status_code = 200
            else:
                self.status_code = 500

        return jsonify(response), self.status_code

    def get_all_sales_records(self, value, option):
        """
        Retrieves all sales records from the database

        Returns:
            tuple: With all sales records and a status code
        """
        response = {}
        response = self.select.select_sales_records(value, option)
        if response.get("msg") == "Empty":
            return jsonify({"msg": "No sales found"}), 404

        if response.get("msg") == "Success":
            self.status_code = 200
        else:
            self.status_code = 500

        return jsonify(response), self.status_code
