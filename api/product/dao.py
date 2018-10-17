import secrets
from flask import jsonify

from api import app
from api.models.product import Product


class ProductController:
    def __init__(self):
        self.status_code = 200
        self.product_list = []

    def add_product(self, request_data):
        """
        Creates a new product in the database

        Args:
            request_data(object): request object holding form data

        Returns:
            tuple: With a response object and a status code
        """
        response = {}
        #  Check if product already exists
        if self.is_product_exists(request_data["name"]):
            response.update({"product": "Product already exists"})
            self.status_code = 409
        else:
            #  Create product
            self.product_list.append(
                Product(id=secrets.token_hex(4), name=request_data["name"], price=request_data["price"]))
            response.update({"msg": "Product added successfully"})
            self.status_code = 200

        return jsonify(response), self.status_code

    def get_all_products(self):
        """
        Retrieves a list of all products from the database

        Returns:
            list: A list of products
        """
        pass

    def is_product_exists(self, product_name):
        """
        Checks if product already exists

        Args:
            product_name(str): Name of the product

        Returns:
            bool: True if exists, False otherwise
        """
        found = False
        if len(self.product_list) > 0:
            for product in self.product_list:
                if product.name == product_name:
                    found = True
                    break
        return found
