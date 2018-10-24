import os
import json
from unittest import TestCase, skip
from datetime import datetime

from api import app
from config import app_settings
from api.models.product import Product
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

    def test_add_product_route(self):
        """Tests add product route"""
        with app.app_context():
            #  Add a new product
            response = self.client.post(
                "/api/v1/products",
                data=dict(
                    name="Flour",
                    price=7000
                ),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": self.access_token
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
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": self.access_token
            }
        )
        self.assertGreater(len(json.loads(res.data)["items"]), 0)

    def test_get_single_product(self):
        """Tests if a single product is fetched from the database"""
        with app.app_context():
            res = self.controller.get_single_product("055ad1fd")
            self.assertEqual(json.loads(res[0].data)["name"], "Milk")

    def test_get_single_product_route(self):
        """Tests that the route gets single product"""
        with app.app_context():
            res = self.client.get(
                "/api/v1/products/{}".format("7bad398f"),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": self.access_token
                }
            )
            self.assertEqual(json.loads(res.data)["name"], "Bread")

    def test_add_stock(self):
        """Tests that the admin can add a stock item"""
        with app.app_context():
            new_stock = dict(
                product_id="539c3032",
                quantity=200
            )
            res = self.controller.add_stock(new_stock)
            self.assertEqual(json.loads(res[0].data)[
                "msg"], "Stock added successfully")

    def test_add_stock_route(self):
        """Tests that the route updates the product stock level"""
        with app.app_context():
            res = self.client.post(
                "/api/v1/products/stock",
                data=dict(
                    product_id="055ad1fd",
                    quantity=500
                ),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": self.access_token
                }
            )
            self.assertEqual(json.loads(res.data)[
                             "msg"], "Stock added successfully")

    def test_edit_product(self):
        """Tests that the admin can edit a product"""
        with app.app_context():
            product_changes = dict(
                product_id="539c3032",
                name="Sugar",
                price=7000,
                min_qty=10
            )
            res = self.controller.edit_product(product_changes)
            self.assertEqual(json.loads(res[0].data)[
                "msg"], "Product updated successfully")

    def test_edit_product_route(self):
        """Tests that the route modifies the product details"""
        with app.app_context():
            product_changes = dict(
                product_id="539c3032",
                name="Sugar",
                price=5000,
                min_qty=7
            )
            res = self.client.post(
                "/api/v1/products/edit/{}".format("539c3032"), 
                data=product_changes,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": self.access_token
                }
            )
            self.assertEqual(json.loads(res.data)[
                "msg"], "Product updated successfully")

    def test_delete_product(self):
        """Tests that the admin can delete a product"""
        with app.app_context():
            #  Add a new product
            response = self.client.post(
                "/api/v1/products",
                data=dict(
                    name="External Hard Disk",
                    price=300000
                ),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": self.access_token
                }
            )
            product_id = json.loads(response.data)["id"]
            #  Delete added product
            res = self.controller.delete_product(product_id)
            self.assertEqual(json.loads(res[0].data)[
                             "msg"], "Product deleted successfully")

    def test_delete_product_route(self):
        """Tests that the route deletes a product from the list"""
        with app.app_context():
            #  Add a new product
            response = self.client.post(
                "/api/v1/products",
                data=dict(
                    name="External Hard Disk",
                    price=300000
                ),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": self.access_token
                }
            )
            product_id = json.loads(response.data)["id"]
            #  Delete added product
            res = self.client.delete(
                "/api/v1/products/delete/{}".format(product_id),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": self.access_token
                }
            )
            self.assertEqual(json.loads(res.data)[
                             "msg"], "Product deleted successfully")

    def test_attendant_cannot_add_product(self):
        """Tests that the attendant cannot add a product"""
        with app.app_context():
            #  Add a new product
            response = self.client.post(
                "/api/v1/products",
                data=dict(
                    name="Laptop Bag",
                    price=150000
                ),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": self.access_token_
                }
            )
            self.assertEqual(
                json.loads(response.data)["msg"], "Admin previlidges required")

    @skip("Not implemented yet")
    def test_attendant_cannot_edit_product(self):
        """Tests that the attendant cannot edit a product"""
        pass

    def test_attendant_cannot_delete_product(self):
        """Tests that the attendant cannot delete a product"""
        with app.app_context():
            res = self.client.delete(
                "/api/v1/products/delete/{}".format("055ad1fd"),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": self.access_token_
                }
            )
            self.assertEqual(json.loads(res.data)[
                             "msg"], "Admin previlidges required")
