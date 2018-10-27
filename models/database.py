from models.user import User
from models.product import Product
from models.cart import Cart
from models.sale import SalesOrder


cart = [
    Cart(id=1, product_id=1, product_name="Sugar", quantity=2, price=4500),
    Cart(id=2, product_id=2, product_name="Milk", quantity=6, price=1500)
]

product_list = [
    Product(id=1, name="Sugar", price=4500, created_at=""),
    Product(id=2, name="Milk", price=1500, created_at=""),
    Product(id=3, name="Bread", price=2700, created_at="")
]

sales_records = [
    SalesOrder(
        id=1,
        user_id=2,
        order_number="de0c1292738aff11",
        created_at=""
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
