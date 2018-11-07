import os
import json
from unittest import TestCase
from datetime import datetime

from api import app
from config.config import app_settings
from models.database_objects import DatabaseObjects
from api.product import controllers


class TestProducts(TestCase):
    def setUp(self):
        app.config.from_object(app_settings[os.environ.get("APP_ENV")])
        self.controller = controllers.ProductController()
        self.db_objects = DatabaseObjects()
        self.client = app.test_client()
        #  Login as admin to get the access token
        response = self.client.post(
            "/api/v1/login",
            json=dict(
                username="admin",
                password="admin"
            ),
            headers={
                "Content-Type": "application/json"
            }
        )
        self.access_token = "Bearer {}".format(
            json.loads(response.data).get("token"))

    def tearDown(self):
        self.db_objects.delete_database_tables()

    def test_add_product_route(self):
        """Tests that the route adds a product to the database"""
        with app.app_context():
            response = self.client.post(
                "/api/v1/products/category",
                json=dict(category_name="Sofas"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
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
                    "Authorization": self.access_token
                }
            )
            self.assertEqual(json.loads(res.data).get("msg"), "Success")
            self.assertTrue(res.status_code, 200)

    def test_is_product_exists(self):
        """Tests that the product exists in the database"""
        with app.app_context():
            response = self.client.post(
                "/api/v1/products/category",
                json=dict(category_name="Dining Tables"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            category_id = json.loads(response.data).get("category").get("id")
            self.client.post(
                "/api/v1/products",
                json=dict(
                    category_id=category_id,
                    product_name="Round Top",
                    product_price=2600000
                ),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            res = self.controller.select.select_single_product(
                "Round Top", category_id)
            self.assertIsNotNone(res)

    def test_get_all_products_route(self):
        """Tests get all products route"""
        with app.app_context():
            response = self.client.post(
                "/api/v1/products/category",
                json=dict(category_name="Corner Stands"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            category_id = json.loads(response.data).get("category").get("id")
            self.client.post(
                "/api/v1/products",
                json=dict(
                    category_id=category_id,
                    product_name="B004",
                    product_price=2600000
                ),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            res = self.client.get(
                "/api/v1/products",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            self.assertEqual(res.status_code, 200)

    def test_get_single_product(self):
        """Tests if a single product is fetched from the database"""
        with app.app_context():
            response = self.client.post(
                "/api/v1/products/category",
                json=dict(category_name="Wall Units"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            category_id = json.loads(response.data).get("category").get("id")
            resp = self.client.post(
                "/api/v1/products",
                json=dict(
                    category_id=category_id,
                    product_name="WU007",
                    product_price=2600000
                ),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            product_id = json.loads(resp.data).get("product").get("id")
            res = self.client.get(
                "/api/v1/products/{}".format(product_id),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            self.assertEqual(json.loads(res.data).get("products")[
                             0].get("product_name"), "WU007")
            self.assertEqual(res.status_code, 200)

    def test_add_stock(self):
        """Tests that the admin can add a stock item"""
        with app.app_context():
            response = self.client.post(
                "/api/v1/products/category",
                json=dict(category_name="Mattresses"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            category_id = json.loads(response.data).get("category").get("id")
            resp = self.client.post(
                "/api/v1/products",
                json=dict(
                    category_id=category_id,
                    product_name="Rose Foam",
                    product_price=2600000
                ),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            product_id = json.loads(resp.data).get("product").get("id")
            result = self.client.post(
                "/api/v1/products/stock",
                json=dict(
                    product_id=product_id,
                    quantity=200
                ),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            self.assertEqual(json.loads(result.data).get("msg"), "Success")
            self.assertEqual(result.status_code, 200)

    def test_edit_product(self):
        """Tests that the admin can edit a product"""
        with app.app_context():
            response = self.client.post(
                "/api/v1/products/category",
                json=dict(category_name="Spring Mattresses"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            category_id = json.loads(response.data).get("category").get("id")
            resp = self.client.post(
                "/api/v1/products",
                json=dict(
                    category_id=category_id,
                    product_name="6x6",
                    product_price=2600000
                ),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            product_id = json.loads(resp.data).get("product").get("id")
            result = self.client.put(
                "/api/v1/products/edit/{}".format(product_id),
                json=dict(
                    category_id=category_id,
                    product_name="6x5",
                    product_price=1500000
                ),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            self.assertEqual(json.loads(result.data).get("msg"), "Success")
            self.assertEqual(result.status_code, 200)

    def test_delete_product(self):
        """Tests that the admin can delete a product"""
        with app.app_context():
            response = self.client.post(
                "/api/v1/products/category",
                json=dict(category_name="Office Chairs"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            category_id = json.loads(response.data).get("category").get("id")
            resp = self.client.post(
                "/api/v1/products",
                json=dict(
                    category_id=category_id,
                    product_name="Executive",
                    product_price=2600000
                ),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            product_id = json.loads(resp.data).get("product").get("id")
            result = self.client.delete(
                "/api/v1/products/delete/{}".format(product_id),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            self.assertEqual(json.loads(result.data).get("msg"), "Success")
            self.assertEqual(result.status_code, 200)

    def test_attendant_cannot_add_product(self):
        """Tests that the attendant cannot add a product"""
        response = self.client.post(
            "/api/v1/products/category",
            json=dict(category_name="Electronics"),
            headers={
                "Content-Type": "application/json",
                "Authorization": self.access_token
            }
        )
        category_id = json.loads(response.data).get("category").get("id")
        res = self.client.post(
            "/api/v1/login",
            json=dict(
                username="Qadie",
                password="attendant"
            ),
            headers={
                "Content-Type": "application/json"
            }
        )
        access_token_ = "Bearer {}".format(json.loads(res.data).get("token"))
        res = self.client.post(
                "/api/v1/products",
                json=dict(
                    category_id=category_id,
                    product_name="Hisence 32inc",
                    product_price=2600000
                ),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": access_token_
                }
            )
        self.assertEqual(json.loads(res.data).get("msg"), "Admin previlidges required")
        self.assertEqual(res.status_code, 403)

    def test_attendant_cannot_edit_product(self):
        """Tests that the attendant cannot edit a product"""
        response = self.client.post(
            "/api/v1/products/category",
            json=dict(category_name="Kitchen Cabinets"),
            headers={
                "Content-Type": "application/json",
                "Authorization": self.access_token
            }
        )
        category_id = json.loads(response.data).get("category").get("id")
        resp = self.client.post(
            "/api/v1/products",
            json=dict(
                category_id=category_id,
                product_name="3 Door",
                product_price=2600000
            ),
            headers={
                "Content-Type": "application/json",
                "Authorization": self.access_token
            }
        )
        product_id = json.loads(resp.data).get("product").get("id")
        res = self.client.post(
            "/api/v1/login",
            json=dict(
                username="Qadie",
                password="attendant"
            ),
            headers={
                "Content-Type": "application/json"
            }
        )
        access_token_ = "Bearer {}".format(json.loads(res.data).get("token"))
        result = self.client.put(
            "/api/v1/products/edit/{}".format(product_id),
            json=dict(
                category_id=category_id,
                product_name="5 Door",
                product_price=1800000

            ),
            headers={
                "Content-Type": "application/json",
                "Authorization": access_token_
            }
        )
        self.assertEqual(json.loads(result.data).get("msg"), "Admin previlidges required")
        self.assertEqual(result.status_code, 403)

    def test_attendant_cannot_delete_product(self):
        """Tests that the attendant cannot delete a product"""
        data = dict(category_name="Office Tables")
        response = self.client.post(
            "/api/v1/products/category",
            json=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": self.access_token
            }
        )
        category_id = json.loads(response.data).get("category").get("id")
        resp = self.client.post(
            "/api/v1/products",
            json=dict(
                category_id=category_id,
                product_name="Executive",
                product_price=2600000
            ),
            headers={
                "Content-Type": "application/json",
                "Authorization": self.access_token
            }
        )
        product_id = json.loads(resp.data).get("product").get("id")
        res = self.client.post(
            "/api/v1/login",
            json=dict(
                username="Qadie", 
                password="attendant"
            ),
            headers={
                "Content-Type": "application/json"
            }
        )
        access_token_ = "Bearer {}".format(json.loads(res.data).get("token"))
        result = self.client.delete(
            "/api/v1/products/delete/{}".format(product_id),
            headers={
                "Content-Type": "application/json",
                "Authorization": access_token_
            }
        )
        self.assertEqual(json.loads(result.data).get("msg"), "Admin previlidges required")
        self.assertEqual(result.status_code, 403)