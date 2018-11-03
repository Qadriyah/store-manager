import json
from unittest import TestCase, skip

from api.sales import controllers
from models.models import SalesOrder, Cart
from api import app


class TestSales(TestCase):

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

    @skip("Needs refactoring")
    def test_add_to_cart(self):
        """Tests that an item is added to the shopping cart"""
        pass

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
