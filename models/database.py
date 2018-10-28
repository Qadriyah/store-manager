from models.user import User
from models.product import Product
from models.cart import Cart
from models.sale import SalesOrder
from models.inventory import Inventory
from models.line_item import LineItem


cart = [
    Cart(id=1, product_id=1, product_name="Sugar", quantity=2, price=4500),
    Cart(id=2, product_id=2, product_name="Milk", quantity=6, price=1500)
]

product_list = [
    Product(id=1, name="Sugar", price=4500, created_at="2018-10-07"),
    Product(id=2, name="Milk", price=1500, created_at="2018-10-07"),
    Product(id=3, name="Bread", price=2700, created_at="2018-10-07")
]

inventories = [
    Inventory(
        id=1,
        product_id=1,
        quantity=50,
        min_quantity=10,
        created_at="2018-10-26",
        updated_at="2018-10-26"
    ),
    Inventory(
        id=2,
        product_id=2,
        quantity=90,
        min_quantity=10,
        created_at="2018-10-26",
        updated_at="2018-10-26"
    ),
    Inventory(
        id=3,
        product_id=3,
        quantity=150,
        min_quantity=10,
        created_at="2018-10-26",
        updated_at="2018-10-26"
    )
]

sales_records = [
    SalesOrder(
        id=1,
        user_id=2,
        order_number="SO-00001",
        created_at="2018-10-26"
    )
]

line_items = [
    LineItem(
        id=1,
        product_id=1,
        sales_id=1,
        product_name="Sugar",
        quantity=2,
        price=4500
    ),
    LineItem(
        id=2,
        product_id=2,
        sales_id=1,
        product_name="Milk",
        quantity=6,
        price=2700
    )
]

users = [
    User(
        id="e9e83c44",
        name="Baker Sekitoleko",
        username="admin",
        password=b'$2b$15$rMjCuBxFGbikgDVgFXkFcu6z8BMrHdUDf7hCr7KAjEef8KIlFTeKa',
        roles="admin",
        created_at=""
    ),
    User(
        id="2067fe34",
        name="Aijuka Miria",
        username="attendant",
        password=b'$2b$15$k9wOjtI8Sgs7hYb93usUEOzW6ugBdqwNEvsfCXuJI2rV9cbCd5En.',
        roles="attendant",
        created_at=""
    )
]
