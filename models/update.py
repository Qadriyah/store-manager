from api import connection


class Update:
    def __init__(self):
        self.cursor = connection.cursor

    def edit_user(self):
        """
        Modifies user details
        """
        pass

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
