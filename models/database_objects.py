from models import connection


class DatabaseObjects:

    def __init__(self):
        db_connect = connection.Connection()
        self.cursor = db_connect.connect()
        self.tables = ["users", "categories", "products",
                       "inventory",  "cart", "salesorder", "line_items", "blacklists"]
        self.create_user_table()
        self.create_category_table()
        self.create_product_table()
        self.create_inventory_table()
        self.create_shopping_cart_table()
        self.create_sales_table()
        self.create_line_items_table()
        self.create_blacklist_table()
        if not self.is_item_exist("username", "users", "admin"):
            self.add_admin_account()
            self.add_default_attendant()
        if not self.is_item_exist("category_name", "categories", "Uncategorized"):
            self.add_default_category()

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
                modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR (15) NOT NULL DEFAULT 'Active'
            );
            """
        )

    def create_category_table(self):
        """Creates the category table"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS categories(
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
                    REFERENCES categories (id)
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
                unit_price INTEGER NOT NULL,
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
                user_id INTEGER NOT NULL, 
                product_id INTEGER NOT NULL,
                product_name VARCHAR (255) NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price INTEGER NOT NULL
            );
            """
        )

    def create_blacklist_table(self):
        """Creates table for blacklisted tokens"""
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS blacklists(
                id SERIAL PRIMARY KEY,
                jti VARCHAR (255) NOT NULL,
                identity VARCHAR (255) NOT NULL,
                expires TIMESTAMP,
                revoked BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
        try:
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
        except Exception:
            print("Server error")

    def add_default_attendant(self):
        """Adds the default admin to the database"""
        try:
            query = """
            INSERT INTO users(fullname, username, password, roles) \
            VALUES('{}', '{}', '{}', '{}')
            """.format(
                "Aijuka Miria",
                "Qadie",
                "$2b$15$/Mhe1jPXUg99JajE76cwaOg8dQyDi7RaOJ/7jZxXuZXFcFphqpxUK",
                "attendant"
            )
            self.cursor.execute(query)
        except Exception:
            print("Server error")

    def add_default_category(self):
        """Adds a default category for uncategorized products"""
        try:
            query = """
            INSERT INTO categories(category_name) VALUES('{}')
            """.format("Uncategorized")
            self.cursor.execute(query)
        except Exception:
            print("Server error")

    def is_item_exist(self, column, table, value):
        """Checks if an item exists in a given table"""
        found = False
        try:
            query = """
            SELECT {} FROM {} WHERE {} = '{}'
            """.format(column, table, column, value)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if result:
                found = True
        except Exception:
            print("Database error")

        return found

    def clear_table(self, table_name):
        """
        Removes items from the shopping cart

        Args:
            table_name(str): Name of the table to be cleared
        """
        try:
            query = """
            DELETE FROM {}
            """.format(table_name)
            self.cursor.execute(query)
        except Exception:
            print("database error")

    def generate_order_number(self, value):
        """
        Generates the order number with leading zeros

        Args:
            value(int): Sales order ID
        """
        response = "0" * (5 - len(str(value)))
        response = "SO-{}{}".format(response, str(value))
        return response
