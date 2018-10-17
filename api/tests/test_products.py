import os
import secrets
import json
from unittest import TestCase
from datetime import datetime

from api import app
from config import app_settings
from api.models.product import Product
from api.product import dao


class TestProducts(TestCase):
    def setUp(self):
        app.config.from_object(app_settings[os.environ.get("APP_ENV")])
        self.controller = dao.ProductController()
        self.controller.product_list = [
            Product(id=secrets.token_hex(4), name="Sugar", price=4500),
            Product(id=secrets.token_hex(4), name="Milk", price=3000),
            Product(id=secrets.token_hex(4), name="Bread", price=2700)
        ]
        self.new_product = {
            "name": "Rice",
            "price": 17000
        }
        self.client = app.test_client()

    def test_add_product_route(self):
        """Tests add product route"""
        response = self.client.post("/api/v1/products", data=dict(
            name="Flour",
            price=7000
        ))
        self.assertEqual(
            json.loads(response.get_data().decode())["msg"],
            "Product added successfully"
        )

    def test_is_product_exists(self):
        """Tests if a product exists in the database"""
        self.assertTrue(self.controller.is_product_exists("Sugar"))

    def test_add_product(self):
        """Test if product list is not empty"""
        with app.app_context():
            self.assertEqual(json.loads(self.controller.add_product(self.new_product)[
                0].get_data().decode("utf-8"))["msg"], "Product added successfully")
