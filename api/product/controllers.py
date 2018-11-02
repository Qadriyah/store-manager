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
                INSERT INTO products(category_id, product_name, product_price) \
                VALUES({}, '{}', {}) RETURNING id
                """.format(
                    data.get("category_id"),
                    data.get("product_name"),
                    data.get("product_price")
                )
                self.cursor.execute(query)
                product_id = self.cursor.fetchone()
                #  Create an entry in the inventory
                self.add_stock(product_id.get("id"))
                response.update({
                    "id": product_id.get("id"),
                    "msg": "Product added successfully"
                })
                self.status_code = 200
            except Exception:
                print("Database error")
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
        SELECT product_name FROM products WHERE product_name = '{}' \
        AND category_id = {} AND status = '{}'
        """.format(product_name, category_id, "Active")
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if not result:
            return None
        return result

    def add_category(self, data):
        """
        creates a product category 

        Args:
            data(object): Hold form data
        """
        response = {}
        if connection.is_item_exist("category", data.get("category_name"), "category_name"):
            response.update({"msg": "Category already exists"})
            self.status_code = 401
        else:
            try:
                query = """
                INSERT INTO category(category_name) \
                VALUES('{}') RETURNING id
                """.format(
                    data.get("category_name")
                )
                self.cursor.execute(query)
                category_id = self.cursor.fetchone()
                response.update({
                    "id": category_id.get("id"),
                    "msg": "Category added successfully"
                })
                self.status_code = 200
            except Exception as error:
                response.update({"msg": "Database error {}".format(error)})
                self.status_code = 500
        return jsonify(response), self.status_code

    def get_all_products(self):
        """
        Retrieves a list of all products from the database

        Returns:
            list: A list of products
        """
        response = {}
        if not connection.is_table_empty("category"):
            response.update({"msg": "No products to display"})
            self.status_code = 404
        try:
            query = """
            SELECT \
                category.category_name, \
                products.product_price, \
                products.product_name, \
                products.id \
            FROM category \
            INNER JOIN products ON category.id = products.category_id \
            WHERE products.status = '{}' ORDER BY products.product_name ASC
            """.format("Active")
            self.cursor.execute(query)
            response = self.cursor.fetchall()
        except Exception:
            return jsonify({"msg": "Database error"}), 500

        return jsonify(response), 200

    def get_single_product(self, product_id):
        """
        Retrieves a single product by product id

        Args:
            product_id(str): Unique product identifier

        Returns:
            tuple: With a response object and a status code
        """
        response = {}
        try:
            query = """
            SELECT \
                category.category_name, \
                products.product_price, \
                products.product_name, \
                products.id \
            FROM category \
            INNER JOIN products ON category.id = products.category_id \
            WHERE products.id = {}
            """.format(product_id)
            self.cursor.execute(query)
            response = self.cursor.fetchone()
            if not response:
                response = {}
                response.update({"msg": "Product does not exist"})
                self.status_code = 404
            self.status_code = 200
        except Exception:
            return jsonify({"msg": "Database error"}), 500
        return jsonify(response), self.status_code

    def add_stock(self, product_id):
        """
        Updates the product quantity

        Args:
            request_data(object): Hold form data
        """
        response = {}
        try:
            query = """
            INSERT INTO inventory(product_id) VALUES({})
            """.format(product_id)
            self.cursor.execute(query)
        except Exception:
            response.update({"msg": "Database error"}), 500

    def update_stock_level(self, data):
        """
        Updates the stock level in case stock is running low

        Args:
            product_id(int): Product to be updated
            quantity(int): Number of units to be added
        """
        response = {}
        try:
            query = """
            UPDATE inventory SET quantity = quantity + {}, \
            stock_level = stock_level + {} WHERE product_id = {}
            """.format(
                data.get("quantity"),
                data.get("quantity"),
                data.get("product_id")
            )
            self.cursor.execute(query)
            response.update({"msg": "Stock updated successfully"})
            self.status_code = 200
        except Exception as error:
            response.update({"msg": "Database error {}".format(error)})
            self.status_code = 500
        return jsonify(response), self.status_code

    def get_stock(self):
        """
        Retrieves stock levels
        """
        response = {}
        try:
            query = """
            SELECT \
                products.id, \
                products.product_name, \
                inventory.quantity, \
                inventory.stock_level, \
                inventory.min_quantity, \
                (SELECT category.category_name FROM category \
                    WHERE category.id = products.category_id) category_name \
            FROM products \
            INNER JOIN inventory ON products.id = inventory.product_id \
            WHERE products.status = '{}' ORDER BY products.product_name ASC
            """.format("Active")
            self.cursor.execute(query)
            response = self.cursor.fetchall()
            if not response:
                response = {}
                response.update({"msg": "No records to display"})
                self.status_code = 404
        except Exception as error:
            response.update({"msg": "Database error {}".format(error)})
            self.status_code = 500
        return jsonify(response), 200

    def delete_product(self, product_id):
        """
        Deletes a product from the product list

        Args:
            product_id(str): Unique product identifier

        Returns:
            tuple: With a response message and a status code
        """
        response = {}
        product_exists = self.get_single_product(product_id)
        if product_exists[1] == 404:
            return product_exists
        try:
            query = """
            UPDATE products SET status = '{}' WHERE id = {}
            """.format("Deleted", product_id)
            self.cursor.execute(query)
            response.update({"msg": "Product deleted successfully"})
            self.status_code = 200

        except Exception:
            response.update({"msg": "Database error"})
            self.status_code = 500
        return jsonify(response), self.status_code

    def edit_product(self, product_id, data):
        """
        Modifies the product details

        Args:
            request_data(object): Hold form data

        Returns:
            tuple: With a response message and a status code
        """
        response = {}
        product_exists = self.get_single_product(product_id)
        if product_exists[1] == 404:
            return product_exists
        try:
            query = """
            UPDATE products SET \
                category_id = {}, \
                product_name = '{}', \
                product_price = {}, \
                modified_at = '{}' \
            WHERE id = {}
            """.format(
                data.get("category_id"),
                data.get("product_name"),
                data.get("product_price"),
                "NOW()",
                product_id
            )
            self.cursor.execute(query)
            response.update({"msg": "Product details updated successfully"})
            self.status_code = 200
        except Exception as error:
            response.update({"msg": "Databse error {}".format(error)})
            self.status_code = 500
        return jsonify(response), self.status_code

    def get_product_categories(self):
        """
        Retrieves products categories
        """
        response = {}
        try:
            query = """
            SELECT id, category_name \
            FROM category WHERE status = '{}' ORDER BY category_name ASC
            """.format("Active")
            self.cursor.execute(query)
            response = self.cursor.fetchall()
            if not response:
                response = {}
                response.update({"msg": "No product categories"})
                self.status_code = 404
            self.status_code = 200
        except Exception:
            response.update({"msg": "Databse error"})
            self.status_code = 500
        return jsonify(response), self.status_code

    def delete_product_category(self, category_id):
        """
        Deletes a product category

        Args:
            category_id(int): Category identifier
        """
        response = {}
        if not connection.is_item_exist("category", category_id, "id"):
            return jsonify({"msg": "Category does not exist"}), 404

        try:
            query = """
            UPDATE category SET status = '{}' WHERE id = {}
            """.format("Deleted", category_id)
            self.cursor.execute(query)
            response.update({"msg": "Category deleted successfully"})
            self.status_code = 200
        except Exception:
            response.update({"msg": "Database error"})
            self.status_code = 500
        return jsonify(response), self.status_code

    def edit_product_category(self, category_id, data):
        """
        Edits product category details
        """
        response = {}
        if not connection.is_item_exist("category", category_id, "id"):
            return jsonify({"msg": "Category does not exist"}), 404

        try:
            query = """
            UPDATE category SET \
                category_name = '{}', modified_at = '{}'::TIMESTAMP \
            WHERE id = {}
            """.format(
                data.get("category_name"),
                "NOW()",
                category_id
            )
            self.cursor.execute(query)
            response.update({"msg": "Product category updated successfully"})
            self.status_code = 200
        except Exception:
            response.update({"msg": "Database error"})
            self.status_code = 500
        return jsonify(response), self.status_code
