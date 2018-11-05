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
            """.format(
                ", ".join(columns),
                table,
                options.get("where"),
                options.get("cell"),
                options.get("order"),
                options.get("sort")
            )
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
            """.format(
                ", ".join(columns),
                table,
                options.get("where"),
                options.get("cell")
            )
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

    def select_all_records_join(self, columns, tables, **options):
        """Retrieves a single record from a given table"""
        response = {}
        try:
            query = """
            SELECT {} FROM {} INNER JOIN {} ON {} = {} WHERE {} = '{}' ORDER BY {} {}
            """.format(
                ", ".join(columns),
                tables[0],
                tables[1],
                options.get("on"),
                options.get("to"),
                options.get("where"),
                options.get("cell"),
                options.get("order"),
                options.get("sort")
            )
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
