from models import connection


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
                name VARCHAR (255) NOT NULL, 
                username VARCHAR (255) UNIQUE NOT NULL, 
                password VARCHAR (255) NOT NULL, 
                roles VARCHAR (20) NOT NULL, 
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
                name VARCHAR (255) NOT NULL, 
                price INTEGER NOT NULL, 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                min_quantity INTEGER DEFAULT 10, 
                created_at DATE NOT NULL, 
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
