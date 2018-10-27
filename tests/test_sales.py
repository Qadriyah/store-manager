import json
import unittest

from api.sales import controllers
from models.cart import Cart
from models.sale import Sale
from models.database import cart
from api import app


class TestSales(unittest.TestCase):

    def setUp(self):
        self.controller = controllers.SalesController()
        self.client = app.test_client()
        self.cart_item = {
            "pid": "7bad398f",
            "name": "Bread",
            "qty": 1,
            "price": 2700
        }
        #  Login to get the access token
        response = self.client.post(
            "/api/v1/login",
            data=dict(
                username="attendant",
                password="attendant"
            ),
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        self.access_token = json.loads(response.data)["token"]

    def tearDown(self):
        pass

    def test_add_to_cart(self):
        """Tests that an item is added to the shopping cart"""
        with app.app_context():
            res = self.controller.add_to_cart(self.cart_item)
            self.assertEqual(json.loads(res[0].data)["msg"], "Success")

    def test_get_cart_items(self):
        """Tests that items are retrieved from the cart"""
        with app.app_context():
            res = self.controller.get_cart_items()
            self.assertGreater(len(json.loads(res[0].data)["items"]), 0)

    def test_is_product_in_cart(self):
        """Tests that the product is already in the shopping cart"""
        #  Add item to the shopping cart
        with app.app_context():
            self.client.post(
                "/api/v1/sales/cart",
                data=dict(
                    pid="055ad1fd",
                    name="Milk",
                    qty=2,
                    price=1500
                ),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": self.access_token
                }
            )
            self.assertTrue(self.controller.is_product_in_cart("Milk"))

    def test_update_qty_in_cart(self):
        """Tests that the quantity of an item in the cart is incremented"""
        res = self.controller.update_qty_in_cart("539c3032", 5)
        self.assertEqual(res, 1)

    def test_is_cart_empty(self):
        """Tests that the shopping cart is not empty"""
        self.assertFalse(self.controller.is_table_empty(cart))

    def test_add_to_cart_route(self):
        """Tests that the route adds an item to the cart"""
        res = self.client.post(
            "/api/v1/sales/cart",
            data=self.cart_item,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": self.access_token
            }
        )
        self.assertEqual(json.loads(res.data)["msg"], "Success")

    def test_get_cart_items_route(self):
        """Tests that the route gets items from the shopping cart"""
        res = self.client.get(
            "/api/v1/sales/cart/items",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": self.access_token
            }
        )
        self.assertGreater(len(json.loads(res.data)["items"]), 0)

    def test_add_sales_record(self):
        """Tests that a sales record is added to the database"""
        with app.app_context():
            res = self.controller.add_sales_record()
            self.assertEqual(json.loads(
                res[0].data)["msg"], "Sales order submitted successfully")

    def test_get_all_sales_records(self):
        """Tests that all sales records are retrieved from the database"""
        with app.app_context():
            res = self.controller.get_all_sales_records()
            self.assertGreater(
                len(json.loads(res[0].data)["items"]), 0)

    def test_get_all_sales_records_route(self):
        """Tests that the route retrieves all sales records"""
        with app.app_context():
            #  Login as admin to get the access token
            response = self.client.post(
                "/api/v1/login",
                data=dict(
                    username="admin",
                    password="admin"
                ),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            access_token = json.loads(response.data)["token"]
            #  Get all sales records
            res = self.client.get(
                "/api/v1/sales",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": access_token
                }
            )
            self.assertGreater(len(json.loads(res.data)["items"]), 0)

    def test_add_sales_record_route(self):
        """Tests that the route adds a sales record to the database"""
        with app.app_context():
            #  Add item to the shopping cart
            self.client.post(
                "/api/v1/sales/cart",
                data=dict(
                    pid="055ad1fd",
                    name="Milk",
                    qty=2,
                    price=1500
                ),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": self.access_token
                }
            )
            #  Add a sales record
            res = self.client.post(
                "/api/v1/sales",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": self.access_token
                }
            )
            self.assertEqual(json.loads(res.data)["msg"],
                             "Sales order submitted successfully")

    def test_admin_cannot_add_to_cart(self):
        """Tests that the admin cannot add items to the shopping cart"""
        with app.app_context():
            #  Login as admin to get the access token
            response = self.client.post(
                "/api/v1/login",
                data=dict(
                    username="admin",
                    password="admin"
                ),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            access_token_ = json.loads(response.data)["token"]
            #  Add item to the cart
            res = self.client.post(
                "/api/v1/sales/cart",
                data=self.cart_item,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": access_token_
                }
            )
            self.assertEqual(json.loads(res.data)["msg"], "Attendants only")
