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
        response = {}
        if len(self.product_list) == 0:
            response.update({"msg": "There are no products"})
            self.status_code = 404
        else:
            items = [
                dict(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    created_at=product.created_at) for product in self.product_list
            ]
            response.update({"items": items})
            self.status_code = 200
        return jsonify(response), self.status_code

    def get_single_product(self, product_id):
        """
        Retrieves a single product by product id

        Args:
            product_id(str): Unique product identifier

        Returns:
            tuple: With a response object and a status code
        """
        response = {}
        found = False
        for product in self.product_list:
            if product.id == product_id:
                response.update({
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "created_at": product.created_at
                })
                found = True
                break
        if found:
            self.status_code = 200
            return jsonify(response), self.status_code

        response.update({"msg": "Product not found"})
        self.status_code = 404
        return jsonify(response), self.status_code

    def is_product_exists(self, product_name):
        """
        Checks if product already exists

        Args:
            product_name(str): Name of the product

        Returns:
            bool: True if exists, False otherwise
        """
        found = False
        if len(self.product_list) == 0:
            return found

        for product in self.product_list:
            if product.name == product_name:
                found = True
                break
        return found
