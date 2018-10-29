from models.user import User
from models.product import Product
from models.cart import Cart
from models.sale import Sale


cart = [
    Cart(pid="539c3032", name="Sugar", qty=2, price=4500),
    Cart(pid="055ad1fd", name="Milk", qty=4, price=1500),
]

product_list = [
    Product(id="539c3032", name="Sugar", price=4500),
    Product(id="055ad1fd", name="Milk", price=1500),
    Product(id="7bad398f", name="Bread", price=2700)
]

sales_records = [
    Sale(
        id="8c2a3bd4",
        user_id="2067fe34",
        order_number="de0c1292738aff11",
        product_id="7bad398f",
        qty=2,
        price=2700,
        product_name="Bread"
    )
]

users = [
    User(
        id="e9e83c44",
        name="Baker Sekitoleko",
        username="admin",
        password=b'$2b$15$rMjCuBxFGbikgDVgFXkFcu6z8BMrHdUDf7hCr7KAjEef8KIlFTeKa',
        roles="admin"
    ),
    User(
        id="2067fe34",
        name="Aijuka Miria",
        username="attendant",
        password=b'$2b$15$k9wOjtI8Sgs7hYb93usUEOzW6ugBdqwNEvsfCXuJI2rV9cbCd5En.',
        roles="attendant"
    )
]
