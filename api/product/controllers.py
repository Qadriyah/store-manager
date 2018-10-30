import secrets
from flask import jsonify

from api import app, connection
from models.models import Product


class ProductController:
    def __init__(self):
        self.status_code = 200
        self.cursor = connection.cursor

    def add_product(self, data):
        """
        Creates a new product in the database

        Args:
            request_data(object): request object holding form data

        Returns:
            tuple: With a response object and a status code
        """
        response = {}
        #  Check if product already exists
        if self.is_product_exists(data.get("product_name"), data.get("category_id")):
            response.update({"product": "Product already exists"})
            self.status_code = 409
        else:
            try:
                #  Create product
                query = """
                INSERT INTO products(category_id, product_name) \
                VALUES({}, '{}')
                """.format(
                    data.get("category_id"),
                    data.get("product_name")
                )
                self.cursor.execute(query)
            except Exception as error:
                print(error)
            result = connection.is_item_exist(
                "products", data.get("product_name"), "product_name")
            response.update({
                "id": result.get("id"),
                "msg": "Product added successfully"
            })
            self.status_code = 200

        return jsonify(response), self.status_code

    def is_product_exists(self, product_name, category_id):
        """
        Checks if the product exists in the database

        Args:
            product_name(str): Name of the product to be checked
            category_id(int): unique identifier of the product category

        Returns:
            object: query result if exists, None otherwise
        """
        query = """
        SELECT product_name FROM products WHERE product_name = '{}' AND category_id = {}
        """.format(product_name, category_id)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if not result:
            return None
        return result

    def add_category(self, data):
        pass

    def get_all_products(self):
        """
        Retrieves a list of all products from the database

        Returns:
            list: A list of products
        """
        pass

    def get_single_product(self, product_id):
        """
        Retrieves a single product by product id

        Args:
            product_id(str): Unique product identifier

        Returns:
            tuple: With a response object and a status code
        """
        pass

    def add_stock(self, request_data):
        """
        Updates the product quantity

        Args:
            request_data(object): Hold form data

        Returns:
            tuple: With a response message and a status code
        """
        pass

    def delete_product(self, product_id):
        """
        Deletes a product from the product list

        Args:
            product_id(str): Unique product identifier

        Returns:
            tuple: With a response message and a status code
        """
        pass

    def edit_product(self, request_data):
        """
        Modifies the product details

        Args:
            request_data(object): Hold form data

        Returns:
            tuple: With a response message and a status code
        """
        pass
