from models import connection
import time
from models import sample_data


class DatabaseObjects:

    def __init__(self):
        db_connect = connection.Connection()
        self.cursor = db_connect.connect()
        self.tables = ["users", "category", "products",
                       "inventory",  "cart", "salesorder", "line_items"]
        self.create_user_table()
        self.create_category_table()
        self.create_product_table()
        self.create_inventory_table()
        self.create_shopping_cart_table()
        self.create_sales_table()
        self.create_line_items_table()
        if not self.is_item_exist("users", "admin", "username"):
            self.add_admin_account()

    def create_user_table(self):
        """Creates a user table"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                fullname VARCHAR (255) NOT NULL,
                username VARCHAR (255) UNIQUE NOT NULL,
                password VARCHAR (255) NOT NULL,
                roles VARCHAR (20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

    def create_category_table(self):
        """Creates the category table"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS category(
                id SERIAL PRIMARY KEY,
                category_name VARCHAR (255) NOT NULL,
                created_at DATE DEFAULT CURRENT_DATE,
                modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR (10) DEFAULT 'Active'
            );
            """
        )

    def create_product_table(self):
        """Creates the product table"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products(
                id SERIAL PRIMARY KEY,
                category_id INTEGER NOT NULL,
                product_name VARCHAR (255) NOT NULL,
                product_price INTEGER NOT NULL,
                created_at DATE DEFAULT CURRENT_DATE,
                modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR (10) DEFAULT 'Active',
                CONSTRAINT product_category_fkey FOREIGN KEY (category_id)
                    REFERENCES category (id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );
            """
        )

    def create_inventory_table(self):
        """Creates the inventory table"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS inventory(
                id SERIAL PRIMARY KEY,
                product_id INTEGER NOT NULL,
                quantity INTEGER DEFAULT 0,
                stock_level INTEGER DEFAULT 0,
                min_quantity INTEGER DEFAULT 10,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT inventory_products_fkey FOREIGN KEY (product_id)
                    REFERENCES products (id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );
            """
        )

    def create_sales_table(self):
        """Creates a sales table"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS salesorder(
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created_at DATE DEFAULT CURRENT_DATE,
                modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

    def create_line_items_table(self):
        """Creates a line_item table"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS line_items(
                id SERIAL PRIMARY KEY,
                product_id INTEGER NOT NULL,
                sales_id INTEGER NOT NULL,
                product_name VARCHAR (255) NOT NULL,
                quantity INTEGER NOT NULL,
                price INTEGER NOT NULL,
                CONSTRAINT line_items_salesorder_fkey FOREIGN KEY (sales_id)
                    REFERENCES salesorder (id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );
            """
        )

    def create_shopping_cart_table(self):
        """Creates a shopping cart table"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cart(
                id SERIAL PRIMARY KEY,
                product_id INTEGER NOT NULL,
                product_name VARCHAR (255) NOT NULL,
                quantity INTEGER NOT NULL,
                price INTEGER NOT NULL
            );
            """
        )

    def delete_database_tables(self):
        """Deletes database tables"""
        for table in self.tables:
            self.cursor.execute(
                """
                DROP TABLE IF EXISTS {} CASCADE
                """.format(table)
            )

    def add_admin_account(self):
        """Adds the default admin to the database"""
        query = """
        INSERT INTO users(fullname, username, password, roles) \
        VALUES('{}', '{}', '{}', '{}')
        """.format(
            "Baker Sekitoleko",
            "admin",
            "$2b$15$rMjCuBxFGbikgDVgFXkFcu6z8BMrHdUDf7hCr7KAjEef8KIlFTeKa",
            "admin"
        )
        self.cursor.execute(query)

    def is_item_exist(self, table_name, item_name, field_name):
        """
        Checks if an item exists in the relation

        Args:
            table_name(str): The target table
            item_name(str): Item to be searched for

        Returns:
            object: Item searched for if found, None otherwise
        """
        query = """
        SELECT * FROM {} WHERE {} = '{}'
        """.format(table_name, field_name, item_name)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if not result:
            return None
        return result

    def is_table_empty(self, table_name):
        """
        Checks if a relation is empty

        Args:
            table_name(str): Name of table to be checked

        Returns:
            bool: True if empty, False otherwise
        """
        query = """
        SELECT * FROM {}
        """.format(table_name)
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        if not result:
            return None
        return result

    def clear_table(self, table_name):
        """
        Removes items from the shopping cart

        Args:
            table_name(str): Name of the table to be cleared
        """
        query = """
        DELETE FROM {}
        """.format(table_name)
        self.cursor.execute(query)

    def add_sample_data(self, table):
        if table == "users":
            for user in sample_data.users:
                self.cursor.execute(
                    """
                        INSERT INTO {}(fullname, username, password, roles)
                            VALUES('{}', '{}', '{}', '{}')
                        """.format(table, user.fullname, user.username, user.password.decode(), user.roles)
                )
        if table == "cart":
            for product in sample_data.cart:
                self.cursor.execute(
                    """
                    INSERT INTO {}(product_id, product_name, quantity, price) 
                        VALUES({}, '{}', {}, {})
                    """.format(table, product.product_id, product.product_name, product.quantity, product.price)
                )
        if table == "inventory":
            for product in sample_data.inventories:
                self.cursor.execute(
                    """
                    INSERT INTO {}(product_id, quantity, stock_level, min_quantity) VALUES({}, {}, {}, {})
                    """.format(table, product.product_id, product.quantity, product.stock_level, product.min_quantity)
                )
        if table == "line_items":
            for product in sample_data.line_items:
                self.cursor.execute(
                    """
                    INSERT INTO {}(product_id, sales_id, product_name, quantity, price) 
                        VALUES({}, {}, '{}', {}, {})
                    """.format(table, product.product_id, product.sales_id, product.product_name, product.quantity, product.price)
                )
        if table == "products":
            for product in sample_data.product_list:
                self.cursor.execute(
                    """
                    INSERT INTO {}(category_id, product_name) VALUES({}, '{}')
                    """.format(table, product.category_id, product.product_name)
                )
        if table == "salesorder":
            for record in sample_data.sales_records:
                self.cursor.execute(
                    """
                    INSERT INTO {}(user_id, order_number, created_at) 
                        VALUES({}, '{}', '{}'::DATE)
                    """.format(table, record.user_id, record.order_number, record.created_at)
                )
        if table == "category":
            for category in sample_data.categories:
                self.cursor.execute(
                    """
                    INSERT INTO {}(category_name, price) \
                    VALUES('{}', {})
                    """.format(table, category.category_name, category.price)
                )
