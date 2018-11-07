import json
import os
from unittest import TestCase, skip

from api.sales.controllers import SalesController
from models.database_objects import DatabaseObjects
from config.config import app_settings
from api import app


class TestSales(TestCase):

    def setUp(self):
        app.config.from_object(app_settings[os.environ.get("APP_ENV")])
        self.controller = SalesController()
        self.db_objects = DatabaseObjects()
        self.client = app.test_client()
        #  Login to get the access token
        resp = self.client.post(
            "/api/v1/login",
            json=dict(
                username="Qadie",
                password="attendant"
            ),
            headers={
                "Content-Type": "application/json"
            }
        )
        self.attendant_token = "Bearer {}".format(
            json.loads(resp.data).get("token"))
        #  Admin login
        res = self.client.post(
            "/api/v1/login",
            json=dict(
                username="admin",
                password="admin"
            ),
            headers={
                "Content-Type": "application/json"
            }
        )
        self.admin_token = "Bearer {}".format(
            json.loads(res.data).get("token"))

    def tearDown(self):
        self.db_objects.delete_database_tables()

    def test_add_to_cart(self):
        """Tests that an item is added to the shopping cart"""
        with app.app_context():
            response = self.client.post(
                "/api/v1/products/category",
                json=dict(category_name="Sofas"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.admin_token
                }
            )
            category_id = json.loads(response.data).get("category").get("id")
            res = self.client.post(
                "/api/v1/products",
                json=dict(
                    category_id=category_id,
                    product_name="PV-160",
                    product_price=2600000
                ),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.admin_token
                }
            )
            product_id = json.loads(res.data).get("product").get("id")
            self.client.post(
                "/api/v1/products/stock",
                json=dict(
                    product_id=product_id,
                    quantity=50
                ),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.admin_token
                }
            )
            resp = self.client.post(
                "/api/v1/sales/cart",
                json=dict(
                    product_id=product_id,
                    quantity=5
                ),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.attendant_token
                }
            )
            self.assertGreater(len(json.loads(resp.data).get("cart")), 0)
            self.assertEqual(resp.status_code, 200)

    @skip("Needs refactoring")
    def test_get_cart_items(self):
        """Tests that items are retrieved from the cart"""
        pass

    @skip("Needs refactoring")
    def test_is_product_in_cart(self):
        """Tests that the product is already in the shopping cart"""
        #  Add item to the shopping cart
        pass

    @skip("Needs refactoring")
    def test_update_qty_in_cart(self):
        """Tests that the quantity of an item in the cart is incremented"""
        pass

    @skip("Needs refactoring")
    def test_is_cart_empty(self):
        """Tests that the shopping cart is not empty"""
        pass

    @skip("Needs refactoring")
    def test_add_to_cart_route(self):
        """Tests that the route adds an item to the cart"""
        pass

    @skip("Needs refactoring")
    def test_get_cart_items_route(self):
        """Tests that the route gets items from the shopping cart"""
        pass

    @skip("Needs refactoring")
    def test_add_sales_record(self):
        """Tests that a sales record is added to the database"""
        pass

    @skip("Needs refactoring")
    def test_get_all_sales_records(self):
        """Tests that all sales records are retrieved from the database"""
        pass

    @skip("Needs refactoring")
    def test_get_all_sales_records_route(self):
        """Tests that the route retrieves all sales records"""
        pass

    @skip("Needs refactoring")
    def test_add_sales_record_route(self):
        """Tests that the route adds a sales record to the database"""
        pass

    @skip("Needs refactoring")
    def test_admin_cannot_add_to_cart(self):
        """Tests that the admin cannot add items to the shopping cart"""
        pass
