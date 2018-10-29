from models import connection, database


class DatabaseObjects:

    def __init__(self):
        db_connect = connection.Connection()
        self.cursor = db_connect.connect()

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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                price INTEGER NOT NULL, 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
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
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
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
                order_number VARCHAR (50) NOT NULL, 
                created_at DATE NOT NULL
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

    def create_shopping_cart(self):
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

    def delete_database_tables(self, table_name):
        """Deletes a database table"""
        self.cursor.execute(
            """
            DROP TABLE IF EXISTS {} CASCADE
            """.format(table_name)
        )

    def add_sample_data(self, table):
        """Adds sample data to postgres database"""
        if table == "users":
            for user in database.users:
                self.cursor.execute(
                    """
                    INSERT INTO {}(fullname, username, password, roles) 
                        VALUES('{}', '{}', '{}', '{}')
                    """.format(table, user.fullname, user.username, user.password.decode(), user.roles)
                )
        if table == "cart":
            for product in database.cart:
                self.cursor.execute(
                    """
                    INSERT INTO {}(product_id, product_name, quantity, price) 
                        VALUES({}, '{}', {}, {})
                    """.format(table, product.product_id, product.product_name, product.quantity, product.price)
                )
        if table == "inventory":
            for product in database.inventories:
                self.cursor.execute(
                    """
                    INSERT INTO {}(product_id, quantity, stock_level, min_quantity) VALUES({}, {}, {}, {})
                    """.format(table, product.product_id, product.quantity, product.stock_level, product.min_quantity)
                )
        if table == "line_items":
            for product in database.line_items:
                self.cursor.execute(
                    """
                    INSERT INTO {}(product_id, sales_id, product_name, quantity, price) 
                        VALUES({}, {}, '{}', {}, {})
                    """.format(table, product.product_id, product.sales_id, product.product_name, product.quantity, product.price)
                )
        if table == "products":
            for product in database.product_list:
                self.cursor.execute(
                    """
                    INSERT INTO {}(category_id, product_name) VALUES({}, '{}')
                    """.format(table, product.category_id, product.product_name)
                )
        if table == "salesorder":
            for record in database.sales_records:
                self.cursor.execute(
                    """
                    INSERT INTO {}(user_id, order_number, created_at) 
                        VALUES({}, '{}', '{}'::DATE)
                    """.format(table, record.user_id, record.order_number, record.created_at)
                )
        if table == "category":
            for category in database.categories:
                self.cursor.execute(
                    """
                    INSERT INTO {}(category_name, price) \
                    VALUES('{}', {})
                    """.format(table, category.category_name, category.price)
                )
