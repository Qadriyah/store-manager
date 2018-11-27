class Update:
    def __init__(self, connection):
        self.cursor = connection.cursor

    def update_user(self, query):
        """
        Modifies user details
        """
        response = {}
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if not result:
                response.update({"msg": "Empty"})
            else:
                response.update({
                    "user": result,
                    "msg": "Success"
                })
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def update_inventory(self, data):
        """
        Updates an inventory
        """
        response = {}
        try:
            query = """
            UPDATE inventory SET quantity = quantity + {}, \
            stock_level = stock_level + {}, modified_at = '{}'::TIMESTAMP \
            WHERE product_id = {} \
            RETURNING product_id, quantity, stock_level, modified_at
            """.format(
                data.get("quantity"),
                data.get("quantity"),
                "NOW()",
                data.get("product_id")
            )
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            response.update({
                "stock": result,
                "msg": "Success"
            })
        except Exception as error:
            print(error)
            response.update({"msg": "Failure"})

        return response

    def update_product(self, product_id, data):
        """
        Updates a product record
        """
        response = {}
        try:
            query = """
            UPDATE products SET \
                category_id = {}, \
                product_name = '{}', \
                product_price = {}, \
                modified_at = '{}' \
            WHERE id = {} \
            RETURNING id, category_id, product_name, product_price, modified_at
            """.format(
                data.get("category_id"),
                data.get("product_name"),
                data.get("product_price"),
                "NOW()",
                product_id
            )
            self.cursor.execute(query)
            response = self.cursor.fetchone()
            response.update({"msg": "Success"})
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def uncategorize_product(self, category_id):
        """
        Updates a product record
        """
        response = {}
        try:
            query = """
            UPDATE products SET category_id = {}, modified_at = '{}' \
            WHERE category_id = {}
            """.format(
                1,
                "NOW()",
                category_id
            )
            self.cursor.execute(query)
            response.update({"msg": "Success"})
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def update_product_category(self, category_id, data):
        """
        Updates a product category
        """
        response = {}
        try:
            query = """
            UPDATE categories \
            SET category_name = '{}', modified_at = '{}' WHERE id = {} \
            RETURNING id, category_name, modified_at
            """.format(
                data.get("category_name"),
                "NOW()",
                category_id
            )
            self.cursor.execute(query)
            response = self.cursor.fetchone()
            response.update({"msg": "Success"})
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def update_stock_level(self, product_id, quantity, operation):
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
            if operation == "del":
                self.cursor.execute(query2)
            if operation == "add":
                self.cursor.execute(query1)
        except Exception:
            print("Database error")

    def update_qty_in_cart(self, product_id, quantity):
        """
        Updates quantity if product is already in the cart

        Args:
            product_id(str): Product identifier
            qty(int): Product quantity
        """
        response = {}
        try:
            query = """
            UPDATE cart SET quantity = quantity + {} WHERE product_id = {} \
            RETURNING id, product_name, quantity, unit_price, (quantity * unit_price) AS total
            """.format(quantity, product_id)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            response.update({
                "cart": result,
                "msg": "Success"
            })
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def update_token(self, jti):
        """Updates the revoked status of the token"""
        response = {}
        try:
            query = """
            UPDATE blacklists SET revoked = '{}'::BOOLEAN WHERE jti = '{}' RETURNING revoked
            """.format(True, jti)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            response.update({
                "revoked": result.get("revoked"),
                "msg": "Success"
            })
        except Exception:
            response.update({"msg": "Failure"})

        return response
