import os
import json
from unittest import TestCase, skip
from datetime import datetime

from api import app
from config.config import app_settings
from models.models import Product
from api.product import controllers


class TestProducts(TestCase):
    def setUp(self):
        app.config.from_object(app_settings[os.environ.get("APP_ENV")])
        self.controller = controllers.ProductController()
        self.client = app.test_client()
        self.new_product = {
            "name": "Rice",
            "price": 17000
        }
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
        self.access_token = json.loads(response.data)["token"]
        #  Login as sales attendant
        res = self.client.post(
            "/api/v1/login",
            data=dict(
                username="attendant",
                password="attendant"
            ),
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        self.access_token_ = json.loads(res.data)["token"]

    @skip("Needs refactoring")
    def test_add_product_route(self):
        """Tests add product route"""
        pass

    @skip("Needs refactoring")
    def test_is_product_exists(self):
        """Tests if a product exists in the database"""
        pass

    @skip("Needs refactoring")
    def test_add_product(self):
        """Test if product list is not empty"""
        pass

    @skip("Needs refactoring")
    def test_get_all_products(self):
        """Tests if products are fetched from the database"""
        pass

    @skip("Needs refactoring")
    def test_get_all_products_route(self):
        """Tests get all products route"""
        pass

    @skip("Needs refactoring")
    def test_get_single_product(self):
        """Tests if a single product is fetched from the database"""
        pass

    @skip("Needs refactoring")
    def test_get_single_product_route(self):
        """Tests that the route gets single product"""
        pass

    @skip("Needs refactoring")
    def test_add_stock(self):
        """Tests that the admin can add a stock item"""
        pass

    @skip("Needs refactoring")
    def test_add_stock_route(self):
        """Tests that the route updates the product stock level"""
        pass

    @skip("Needs refactoring")
    def test_edit_product(self):
        """Tests that the admin can edit a product"""
        pass

    @skip("Needs refactoring")
    def test_edit_product_route(self):
        """Tests that the route modifies the product details"""
        pass

    @skip("Needs refactoring")
    def test_delete_product(self):
        """Tests that the admin can delete a product"""
        pass

    @skip("Needs refactoring")
    def test_delete_product_route(self):
        """Tests that the route deletes a product from the list"""
        pass

    @skip("Needs refactoring")
    def test_attendant_cannot_add_product(self):
        """Tests that the attendant cannot add a product"""
        pass

    @skip("Needs refactoring")
    def test_attendant_cannot_edit_product(self):
        """Tests that the attendant cannot edit a product"""
        pass

    @skip("Needs refactoring")
    def test_attendant_cannot_delete_product(self):
        """Tests that the attendant cannot delete a product"""
        pass
