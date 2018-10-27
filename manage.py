import time

from models import database_objects
from api import manager


db_object = database_objects.DatabaseObjects()
tables = ["users", "cart", "inventory", "line_items", "products", "salesorder"]


@manager.command
def create_tables():
    """Creates database tables"""
    print("[+] Creating users table...")
    db_object.create_user_table()
    time.sleep(1)
    print("[+] Creating products table...")
    db_object.create_product_table()
    time.sleep(1)
    print("[+] Creating inventory table...")
    db_object.create_inventory_table()
    time.sleep(1)
    print("[+] Creating salesorder table...")
    db_object.create_sales_table()
    time.sleep(1)
    print("[+] Creating line_items table...")
    db_object.create_line_items_table()
    time.sleep(1)
    print("[+] Creating shopping_cart table...")
    db_object.create_shopping_cart()
    time.sleep(1)
    print("[+] Tables created successfully")


@manager.command
def delete_tables():
    """Deletes all database tables"""
    for table in tables:
        print("[+] Deleting table {}...".format(table))
        db_object.delete_database_tables(table)
        time.sleep(1)
    print("[+] Tables deleted successfully")


if __name__ == "__main__":
    manager.run()
