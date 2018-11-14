from datetime import datetime


class Insert:
    def __init__(self, connection):
        self.cursor = connection.cursor

    def insert_user(self, user):
        """Inserts a record in the users table"""
        response = {}
        try:
            query = """
            INSERT INTO users(fullname, username, password, roles) \
            VALUES('{}', '{}', '{}', '{}') 
            RETURNING id, fullname, username, roles, created_at
            """.format(
                user.get("fullname"),
                user.get("username"),
                user.get("password"),
                user.get("roles")
            )
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            response.update({
                "user": result,
                "msg": "Success"
            })
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def insert_category(self, category):
        """
        Inserts a record in the categories table
        """
        response = {}
        try:
            query = """
            INSERT INTO categories(category_name) VALUES('{}') \
            RETURNING id, category_name, created_at
            """.format(category.get("category_name"))
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            response.update({
                "category": result,
                "msg": "Success"
            })
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def insert_product(self, product):
        """
        Inserts a record in the products table
        """
        response = {}
        try:
            #  Create product
            query = """
            INSERT INTO products(category_id, product_name, product_price) \
            VALUES({}, '{}', {}) 
            RETURNING id, category_id, product_name, product_price, created_at
            """.format(
                product.get("category_id"),
                product.get("product_name"),
                product.get("product_price")
            )
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            #  Create an entry in the inventory
            self.insert_inventory(result.get("id"))
            response.update({
                "product": result,
                "msg": "Success"
            })
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def insert_inventory(self, product_id):
        """Inserts a record in the inventory table"""
        try:
            query = """
            INSERT INTO inventory(product_id) VALUES({})
            """.format(product_id)
            self.cursor.execute(query)
        except Exception:
            print("Database error")

    def insert_cart(self, cart):
        """Inserts a record in the cart table"""
        response = {}
        try:
            query = """
            INSERT INTO cart(product_id, user_id, product_name, quantity, unit_price) \
            VALUES({}, {}, '{}', {}, {}) 
            RETURNING id, product_name, quantity, unit_price, (quantity * unit_price) AS total
            """.format(
                cart.get("product_id"),
                cart.get("user_id"),
                cart.get("product_name"),
                cart.get("quantity"),
                cart.get("product_price")
            )
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            response.update({
                "cart": result,
                "msg": "Success"
            })
        except Exception as error:
            print(error)
            response.update({"msg": "Failure"})

        return response

    def insert_salesorder(self, salesorder):
        """Inserts a record in the salesorder table"""
        response = {}
        items = []
        try:
            query = """
            INSERT INTO salesorder(user_id) VALUES({}) RETURNING id
            """.format(salesorder.get("user_id"))
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            #  Insert the line items
            sales_id = result.get("id")
            for product in salesorder.get("cart"):
                item = self.insert_line_items(product, sales_id)
                items.append(item.get("cart"))

            response.update({
                "id": result.get("id"),
                "sales_order": result,
                "items": items,
                "msg": "Success"
            })
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def insert_line_items(self, product, sales_id):
        """Inserts a record into the line_items table"""
        response = {}
        try:
            query = """
            INSERT INTO line_items(product_id, sales_id, product_name, quantity, unit_price) VALUES({}, {}, '{}', {}, {}) \
            RETURNING sales_id, product_name, quantity, unit_price, (quantity * unit_price) AS total
            """.format(
                product.get("product_id"),
                sales_id,
                product.get("product_name"),
                product.get("quantity"),
                product.get("unit_price")
            )
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            response.update({
                "cart": result,
                "msg": "Success"
            })
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def insert_blacklist(self, token):
        """Inserts a blacklisted token"""
        response = {}
        try:
            query = """
            INSERT INTO blacklists(jti, identity, expires) \
            VALUES('{}', '{}', '{}'::TIMESTAMP) RETURNING id, jti, identity, expires
            """.format(token.get("jti"), token.get("identity"), datetime.fromtimestamp(token.get("exp")))
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            response.update({
                "token": result,
                "msg": "Success"
            })
        except Exception as error:
            print(error)
            response.update({"msg": "Failure"})

        return response
