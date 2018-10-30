import secrets
from flask import jsonify

from api import app
from models.models import Product


class ProductController:
    def __init__(self):
        self.status_code = 200

    ''' def add_product(self, request_data):
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
            new_product = Product(
                id=secrets.token_hex(4),
                name=request_data["name"],
                price=request_data["price"]
            )
            product_list.append(new_product)
            response.update({"id": str(new_product.id)})
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
        if len(product_list) == 0:
            response.update({"msg": "There are no products"})
            self.status_code = 404
        else:
            items = [
                dict(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    created_at=product.created_at) for product in product_list
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
        for product in product_list:
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
        if len(product_list) == 0:
            return found

        for product in product_list:
            if product.name == product_name:
                found = True
                break
        return found

    def add_stock(self, request_data):
        """
        Updates the product quantity

        Args:
            request_data(object): Hold form data

        Returns:
            tuple: With a response message and a status code
        """
        response = {}
        found = False
        for product in product_list:
            if product.id == request_data["product_id"]:
                temp = int(product.quantity)
                temp += int(request_data["quantity"])
                product.quantity = str(temp)
                found = True
                break
        if not found:
            response.update({"msg": "No product was selected"})
            self.status_code = 404
        else:
            response.update({"msg": "Stock added successfully"})
            self.status_code = 200
        return jsonify(response), self.status_code

    def delete_product(self, product_id):
        """
        Deletes a product from the product list

        Args:
            product_id(str): Unique product identifier

        Returns:
            tuple: With a response message and a status code
        """
        response = {}
        deleted = False
        for product in product_list:
            if product.id == product_id:
                product_list.remove(product)
                deleted = True
                break
        if deleted:
            response.update({"msg": "Product deleted successfully"})
            self.status_code = 200
        else:
            response.update({"msg": "Product not found"})
            self.status_code = 404

        return jsonify(response), self.status_code

    def edit_product(self, request_data):
        """
        Modifies the product details

        Args:
            request_data(object): Hold form data

        Returns:
            tuple: With a response message and a status code
        """
        response = {}
        modified = False
        for product in product_list:
            if product.id == request_data["product_id"]:
                product.name = request_data["name"]
                product.price = request_data["price"]
                modified = True
                break
        if modified:
            response.update({"msg": "Product updated successfully"})
            self.status_code = 200
        else:
            response.update({"msg": "Product not found"})
            self.status_code = 404

        return jsonify(response), self.status_code
 '''
