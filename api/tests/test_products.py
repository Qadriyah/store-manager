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
        self.product_id = secrets.token_hex(4)
        self.controller.product_list = [
            Product(id=secrets.token_hex(4), name="Sugar", price=4500),
            Product(id=secrets.token_hex(4), name="Milk", price=3000),
            Product(id=secrets.token_hex(4), name="Bread", price=2700),
            Product(id=self.product_id, name="Flour", price=7000)
        ]
        self.new_product = {
            "name": "Rice",
            "price": 17000
        }
        self.client = app.test_client()

    def test_add_product_route(self):
        """Tests add product route"""
        response = self.client.post(
            "/api/v1/products",
            data=dict(
                name="Flour",
                price=7000
            ),
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        self.assertEqual(
            json.loads(response.data)["msg"], "Product added successfully")

    def test_is_product_exists(self):
        """Tests if a product exists in the database"""
        self.assertTrue(self.controller.is_product_exists("Sugar"))

    def test_add_product(self):
        """Test if product list is not empty"""
        with app.app_context():
            res = self.controller.add_product(self.new_product)
            self.assertEqual(json.loads(res[0].data)[
                             "msg"], "Product added successfully")

    def test_get_all_products(self):
        """Tests if products are fetched from the database"""
        with app.app_context():
            res = self.controller.get_all_products()
            self.assertGreater(len(json.loads(res[0].data)["items"]), 0)

    def test_get_all_products_route(self):
        """Tests get all products route"""
        res = self.client.get(
            "/api/v1/products",
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        self.assertGreater(len(json.loads(res.data)["items"]), 0)

    def test_get_single_product(self):
        """Tests if a single product is fetched from the database"""
        with app.app_context():
            res = self.controller.get_single_product(self.product_id)
            self.assertEqual(json.loads(res[0].data)["name"], "Flour")

    def test_get_single_product_route(self):
        """Tests get single product route"""
        with app.app_context():
            response = self.client.post(
                "/api/v1/products",
                data=dict(
                    name="iPhone",
                    price=900000
                ),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            product_id = json.loads(response.data)["id"]
            res = self.client.get(
                "/api/v1/products/{}".format(product_id),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            self.assertEqual(json.loads(res.data)["name"], "iPhone")
