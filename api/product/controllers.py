from flask import jsonify

from api import app, connection
from models.select import Select
from models.insert import Insert
from models.delete import Delete
from models.update import Update


class ProductController:
    def __init__(self):
        self.status_code = 200
        self.cursor = connection.cursor
        self.insert = Insert()
        self.select = Select()
        self.delete = Delete()
        self.update = Update()

    def add_category(self, data):
        """
        creates a product category 

        Args:
            data(object): Hold form data
        """
        response = {}
        if connection.is_item_exist("category_name", "categories", data.get("category_name")):
            response.update({"msg": "Category already exists"})
            self.status_code = 401
        else:
            response = self.insert.insert_category(data)
            if response.get("msg") == "Success":
                self.status_code = 200
            else:
                response.update({"msg": "Some fields are missing"})
                self.status_code = 500

        return jsonify(response), self.status_code

    def get_product_categories(self):
        """
        Retrieves products categories
        """
        response = {}
        columns = ["id", "category_name"]
        result = self.select.select_all_records(
            columns, "categories", where="status", cell="Active",
            order="category_name", sort="ASC")

        if result.get("msg") == "Empty":
            response.update({"msg": "No product categories found"})
            self.status_code = 404

        elif result.get("msg") == "Failure":
            response.update({"msg": "Server error"})
            self.status_code = 500

        else:
            response = result
            self.status_code = 200

        return jsonify(response), self.status_code

    def add_product(self, data):
        """
        Creates a new product in the database
        """
        response = {}
        #  Check if product already exists
        if self.select.select_single_product(data.get("product_name"), data.get("category_id")):
            response.update({"product": "Product already exists"})
            self.status_code = 401
        else:
            response = self.insert.insert_product(data)
            if response.get("msg") == "Success":
                self.status_code = 200
            else:
                response.update({"msg": "Server error"})
                self.status_code = 500

        return jsonify(response), self.status_code

    def get_all_products(self):
        """
        Retrieves a list of all products from the database

        Returns:
            list: A list of products
        """
        response = {}
        columns = ["categories.category_name", "products.product_price", "products.product_name", "products.id"]
        result = self.select.select_all_records_join(columns, ["categories", "products"], on="categories.id", to="products.category_id", where="products.status", cell="Active", order="products.product_name", sort="ASC")
        
        if result.get("msg") == "Success":
            response = result
            self.status_code = 200

        if result.get("msg") == "Empty":
            response.update({"msg": "No products to found"})
            self.status_code = 404

        if result.get("msg") == "Failure":
            response.update({"msg": "Database error"})
            self.status_code = 500

        return jsonify(response), self.status_code

    def get_single_product(self, product_id):
        """
        Retrieves a single product by product id
        """
        response = {}
        columns = ["categories.category_name", "products.product_price", "products.product_name", "products.id"]
        result = self.select.select_all_records_join(columns, ["categories", "products"], on="categories.id", to="products.category_id", where="products.id", cell=product_id, order="products.product_name", sort="ASC")
        
        if result.get("msg") == "Success":
            response = result
            self.status_code = 200

        if result.get("msg") == "Empty":
            response.update({"msg": "No products to found"})
            self.status_code = 404

        if result.get("msg") == "Failure":
            response.update({"msg": "Database error"})
            self.status_code = 500

        return jsonify(response), self.status_code


    def update_stock_level(self, data):
        """
        Updates the stock level in case stock is running low

        Args:
            product_id(int): Product to be updated
            quantity(int): Number of units to be added
        """
        response = {}
        if data.get("quantity") <= 0:
            response.update({"msg": "Quantity should be greater than zero"})
            return jsonify(response), 401

        response = self.update.update_inventory(data)
        if response.get("msg") == "Success":
            self.status_code = 200
        else:
            self.status_code = 500
        
        return jsonify(response), self.status_code

    def get_stock(self):
        """
        Retrieves stock levels
        """
        response = {}
        result = self.select.select_stock_level()
        if result.get("msg") == "Empty":
            response.update({"msg": "No records found"})
            self.status_code = 404

        if result.get("msg") == "Failure":
            response.update({"msg": "Server error"})
            self.status_code = 500

        if result.get("msg") == "Success":
            response = result
            self.status_code = 200

        return jsonify(response), self.status_code

    def delete_product(self, product_id):
        """
        Deletes a product from the product list
        """
        response = {}
        if not connection.is_item_exist("id", "products", product_id):
            response.update({"msg": "Product does not exist"})
            self.status_code = 404

        response = self.delete.delete_record("products", product_id)
        if response.get("msg") == "Success":
            self.status_code = 200
        else:
            self.status_code = 500
        
        return jsonify(response), self.status_code

    def edit_product(self, product_id, data):
        """
        Modifies the product details
        """
        response = {}
        if not connection.is_item_exist("id", "products", product_id):
            response.update({"msg": "Product does not exist"})
            return jsonify(response), 404

        if not connection.is_item_exist("id", "categories", data.get("category_id")):
            response.update({"msg": "Category does not exist"})
            return jsonify(response), 404

        response = self.update.update_product(product_id, data)
        if response.get("msg") == "Success":
            self.status_code = 200
        else:
            self.status_code = 500
        
        return jsonify(response), self.status_code

    def delete_product_category(self, category_id):
        """
        Deletes a product category

        Args:
            category_id(int): Category identifier
        """
        response = {}
        if not connection.is_item_exist("id", "categories", category_id):
            response.update({"msg": "Category does not exist"})
            return jsonify(response), 404

        response = self.delete.delete_record("categories", category_id)
        if response.get("msg") == "Success":
            self.update.uncategorize_product(category_id)
            self.status_code = 200
        else:
            self.status_code = 500

        return jsonify(response), self.status_code

    def edit_product_category(self, category_id, data):
        """
        Edits product category details
        """
        response = {}
        if not connection.is_item_exist("id", "categories", category_id):
            response.update({"msg": "Category does not exist"})
            return jsonify(response), 404

        response = self.update.update_product_category(category_id, data)
        if response.get("msg") == "Success":
            self.status_code = 200
        else:
            self.status_code = 500
        
        return jsonify(response), self.status_code
