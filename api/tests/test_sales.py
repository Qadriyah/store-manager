import secrets
import json
from unittest import TestCase

from api.sales import dao
from api.models.cart import Cart
from api import app


class TestSales(TestCase):

    def setUp(self):
        self.controller = dao.SalesController()
        self.client = app.test_client()
        self.cart_item = {
            "pid": secrets.token_hex(4),
            "name": "Milk",
            "qty": 2,
            "price": 1500
        }
        self.product_id = secrets.token_hex(4)
        self.controller.cart = [
            Cart(pid=secrets.token_hex(4), name="Sugar", qty=2, price=4500),
            Cart(pid=secrets.token_hex(4), name="Milk", qty=4, price=1500),
            Cart(pid=self.product_id, name="Rice", qty=1, price=17000)
        ]

    def test_add_to_cart(self):
        """Tests that an item is added to the shopping cart"""
        self.assertEqual(self.controller.add_to_cart(
            self.cart_item), "Success")

    def test_get_cart_items(self):
        """Tests that items are retrieved from the cart"""
        with app.app_context():
            res = self.controller.get_cart_items()
            self.assertGreater(len(json.loads(res[0].data)["items"]), 0)

    def test_is_product_in_cart(self):
        """Tests that the product is already in the shopping cart"""
        self.assertTrue(self.controller.is_product_in_cart("Sugar"))

    def test_update_qty_in_cart(self):
        """Tests that the quantity of an item in the cart is incremented"""
        res = self.controller.update_qty_in_cart(self.product_id, 5)
        self.assertEqual(res, 1)

    def test_is_cart_empty(self):
        """Tests that the shopping cart is not empty"""
        self.assertFalse(self.controller.is_cart_empty())

    def test_add_to_cart_route(self):
        """Tests that the route adds an item to the cart"""
        res = self.client.post("/api/v1/sales/cart", data=dict(
            pid=secrets.token_hex(4),
            name="Milk",
            qty=2,
            price=1500
        ))
        self.assertEqual(res.data.decode(), "Success")

    def test_get_cart_items_route(self):
        """Tests that the route gets items from the shopping cart"""
        res = self.client.get("/api/v1/sales/cart/items")
        self.assertGreater(len(json.loads(res.data)["items"]), 0)

    def test_add_sales_record(self):
        """Tests that a sales record is added to the database"""
        with app.app_context():
            res = self.controller.add_sales_record()
            self.assertEqual(json.loads(
                res[0].data)["msg"], "Sales order submitted successfully")

    ''' def test_add_sales_record_route(self):
        """Tests that the route adds a sales record to the database"""
        res = self.client.post("/api/v1/sales")
        self.assertEqual(json.loads(res.data.decode())["cart"],
                         "Sales order submitted successfully") '''
