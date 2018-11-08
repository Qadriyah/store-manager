from api import connection


class Select:
    def __init__(self):
        self.cursor = connection.cursor

    def select_all_records(self, columns, table, **options):
        """Retrieves all records from a given table"""
        response = {}
        try:
            query = """
            SELECT {} FROM {} WHERE {} = '{}' ORDER BY {} {}
            """.format(", ".join(columns), table, options.get("where"),
                       options.get("cell"), options.get("order"), options.get("sort"))
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            if not result:
                response.update({"msg": "Empty"})
            else:
                response.update({
                    table: result,
                    "msg": "Found"
                })
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def select_single_record(self, columns, table, **options):
        """Retrieves a single record from a given table"""
        response = {}
        try:
            query = """
            SELECT {} FROM {} WHERE {} = {}
            """.format(", ".join(columns), table, options.get("where"),
                       options.get("cell"))
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if not result:
                response.update({"msg": "Empty"})
            else:
                response.update({
                    table: result,
                    "msg": "Found"
                })
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def select_all_records_join(self, columns, tables, **options):
        """Retrieves a single record from a given table"""
        response = {}
        try:
            query = """
            SELECT {} FROM {} INNER JOIN {} ON {} = {} WHERE {} = '{}' ORDER BY {} {}
            """.format(", ".join(columns), tables[0], tables[1], options.get("on"),
                       options.get("to"), options.get(
                           "where"), options.get("cell"),
                       options.get("order"), options.get("sort"))
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            if not result:
                response.update({"msg": "Empty"})
            else:
                response.update({
                    "products": result,
                    "msg": "Success"
                })
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def select_single_product(self, product_name, category_id):
        """
        Retrieves a record from the table using two fields
        """
        found = False
        try:
            query = """
            SELECT id, product_name FROM products WHERE product_name = '{}' \
            AND category_id = {} AND status = '{}'
            """.format(
                product_name,
                category_id,
                "Active"
            )
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if result:
                found = True
        except Exception:
            print("Database error")

        return found

    def select_stock_level(self):
        """Retrieves all records from the inventory"""
        response = {}
        try:
            query = """
            SELECT \
                products.id, products.product_name, inventory.quantity, \
                inventory.stock_level, inventory.min_quantity, \
                (SELECT categories.category_name FROM categories \
                    WHERE categories.id = products.category_id) category_name \
            FROM products \
            INNER JOIN inventory ON products.id = inventory.product_id \
            WHERE products.status = '{}' ORDER BY products.product_name ASC
            """.format("Active")
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            if not result:
                response.update({"msg": "Empty"})
            else:
                response.update({
                    "stock": result,
                    "msg": "Success"
                })
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def select_single_stock_level(self, product_id):
        """Retrieves all records from the inventory"""
        response = {}
        try:
            query = """
            SELECT \
                products.id, products.product_name, products.product_price, \
                inventory.quantity, inventory.stock_level, inventory.min_quantity, \
                (SELECT categories.category_name FROM categories \
                    WHERE categories.id = products.category_id) category_name \
            FROM products \
            INNER JOIN inventory ON products.id = inventory.product_id \
            WHERE products.status = '{}' AND products.id = {}
            """.format("Active", product_id)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if not result:
                response.update({"msg": "Empty"})
            else:
                response.update({
                    "stock": result,
                    "msg": "Success"
                })
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def select_cart_items(self, user_id):
        response = {}
        try:
            query = """
            SELECT id, product_id, product_name, quantity, unit_price, \
            (quantity * unit_price) AS total FROM cart WHERE user_id = {}
            """.format(user_id)
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            if not result:
                response.update({"msg": "Empty"})
            else:
                response.update({
                    "cart": result,
                    "msg": "Success"
                })

        except Exception:
            response.update({"msg": "Failure"})

        return response

    def select_single_cart_item(self, cart_id):
        response = {}
        try:
            query = """
            SELECT id, product_id, quantity, unit_price FROM cart WHERE id = {}
            """.format(cart_id)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if not result:
                response.update({"msg": "Empty"})
            else:
                response.update({"cart": result, "msg": "Success"})

        except Exception:
            response.update({"msg": "Failure"})

        return response

    def select_sales_records(self, value, option):
        response = {}
        orders = []
        try:
            query = """
            SELECT id, user_id, created_at FROM salesorder ORDER BY created_at DESC
            """
            query1 = """
            SELECT id, user_id, created_at FROM salesorder WHERE id = {}
            """.format(value)
            query2 = """
            SELECT id, user_id, created_at FROM salesorder WHERE user_id = {} \
            ORDER BY created_at DESC
            """.format(value)
            if option == "single":
                self.cursor.execute(query1)
            elif option == "user":
                self.cursor.execute(query2)
            else:
                self.cursor.execute(query)
            sales_orders = self.cursor.fetchall()
            for item in sales_orders:
                temp = {}
                temp.update({
                    "id": item.get("id"),
                    "order_number": connection.generate_order_number(item.get("id")),
                    "order_date": item.get("created_at"),
                    "sold_by": self.select_single_record(["fullname"], "users", where="id", cell=item.get("user_id")).get("fullname"),
                    "items": self.get_line_items(item.get("id"))
                })
                orders.append(temp)
            if len(orders) > 0:
                response.update({"orders": orders, "msg": "Success"})
            else:
                response.update({"msg": "Empty"})
        except Exception:
            response.update({"msg": "Failure"})

        return response

    def get_line_items(self, sales_id):
        response = {}
        try:
            query = """
            SELECT *, (quantity * unit_price) AS total FROM line_items \
            WHERE sales_id = {}
            """.format(sales_id)
            self.cursor.execute(query)
            response = self.cursor.fetchall()
        except Exception:
            print("Failure")
        return response
