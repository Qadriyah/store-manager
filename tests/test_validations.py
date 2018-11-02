import os
import json
from unittest import TestCase

from models.database_objects import DatabaseObjects
from config.config import app_settings
from api import app


class TestValidations(TestCase):

    def setUp(self):
        app.config.from_object(app_settings[os.environ.get("APP_ENV")])
        self.db_objects = DatabaseObjects()
        self.client = app.test_client()
        data = dict(
            username="admin",
            password="admin"
        )
        response = self.client.post(
            "/api/v1/login",
            json=data,
            headers={
                "Content-Type": "application/json"
            }
        )
        self.access_token = "Bearer {}".format(
            json.loads(response.data)["token"])

    def tearDown(self):
        self.db_objects.delete_database_tables()

    def test_empty_text_fields(self):
        """Tests that an input field is empty"""
        with app.app_context():
            product = dict(
                category_id="",
                product_name="",
                product_price=""
            )
            res = self.client.post(
                "/api/v1/products",
                json=product,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            self.assertEqual(res.status_code, 400)

    def test_field_does_not_exixts(self):
        """Tests that an input field does not exist"""
        with app.app_context():
            product = dict()
            res = self.client.post(
                "/api/v1/products",
                json=product,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            self.assertEqual(res.status_code, 400)

    def test_value_entered_in_integer_fields(self):
        """Tests that the value in the number field is not integers"""
        with app.app_context():
            product = dict(
                category_id="KK",
                product_name="iPhone X",
                product_price="5000000G"
            )
            res = self.client.post(
                "/api/v1/products",
                json=product,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            self.assertEqual(res.status_code, 400)

    def test_url_parameter(self):
        """Tests that the number passed as a url parameter is not integer"""
        with app.app_context():
            res = self.client.get(
                "/api/v1/products/k",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.access_token
                }
            )
            self.assertEqual(json.loads(res.data)[
                             "msg"], "Product Id should be an integer")
            self.assertEqual(res.status_code, 400)
