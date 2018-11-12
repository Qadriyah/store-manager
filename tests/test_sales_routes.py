import json
import os
from unittest import TestCase
from flask_jwt_extended import current_user

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

    def test_get_cart_items(self):
        """Tests that items are retrieved from the cart"""
        with app.app_context():
            response = self.client.post(
                "/api/v1/products/category",
                json=dict(category_name="Electronics"),
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
                    product_name="Hisence 42inc",
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
            self.client.post(
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
            resp = self.client.get(
                "/api/v1/sales/cart",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.attendant_token
                }
            )
            self.assertGreater(len(json.loads(resp.data).get("cart")), 0)
            self.assertEqual(resp.status_code, 200)

    def test_out_of_stock(self):
        """Tests that the product being added to the shopping cart is out of stock"""
        with app.app_context():
            response = self.client.post(
                "/api/v1/products/category",
                json=dict(category_name="Beds"),
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
                    product_name="Bed 406",
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
                    quantity=70
                ),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.attendant_token
                }
            )
            self.assertEqual(json.loads(resp.data).get(
                "msg"), "Product is out of stock")
            self.assertEqual(resp.status_code, 401)

    def test_prouduct_does_not_exists(self):
        """Tests that the product being added to the cart does not exists"""
        with app.app_context():
            resp = self.client.post(
                "/api/v1/sales/cart",
                json=dict(
                    product_id=10,
                    quantity=2
                ),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.attendant_token
                }
            )
            self.assertEqual(json.loads(resp.data).get(
                "msg"), "Product does not exist")
            self.assertEqual(resp.status_code, 404)

    def test_is_cart_empty(self):
        """Tests that the shopping cart is empty"""
        with app.app_context():
            resp = self.client.get(
                "/api/v1/sales/cart",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.attendant_token
                }
            )
            self.assertEqual(json.loads(resp.data).get(
                "msg"), "No items in the shopping cart")
            self.assertEqual(resp.status_code, 404)

    def test_add_sales_record(self):
        """Tests that a sales record is added to the database"""
        with app.app_context():
            response = self.client.post(
                "/api/v1/products/category",
                json=dict(category_name="Burnners"),
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
                    product_name="Solstar 4 Bunner",
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
            self.client.post(
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
            result = self.client.post(
                "/api/v1/sales",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.attendant_token
                }
            )
            self.assertEqual(json.loads(result.data).get("msg"), "Success")
            self.assertEqual(result.status_code, 200)

    def test_get_all_sales_records(self):
        """Tests that all sales records are retrieved from the database"""
        with app.app_context():
            response = self.client.post(
                "/api/v1/products/category",
                json=dict(category_name="Bookshelves"),
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
                    product_name="BS-1900",
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
            self.client.post(
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
            self.client.post(
                "/api/v1/sales",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.attendant_token
                }
            )
            result = self.client.get(
                "/api/v1/sales",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.admin_token
                }
            )
            self.assertEqual(json.loads(result.data).get("msg"), "Success")
            self.assertEqual(result.status_code, 200)

    def test_delete_cart_item(self):
        """Tests that an item is deleted from the cart"""
        with app.app_context():
            response = self.client.post(
                "/api/v1/products/category",
                json=dict(category_name="Garden Sets"),
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
                    product_name="2 Seater",
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
            card_id = json.loads(resp.data).get("cart")[0].get("id")
            result = self.client.delete(
                "/api/v1/sales/cart/delete/{}".format(card_id),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.attendant_token
                }
            )
            self.assertEqual(json.loads(result.data).get(
                "msg"), "Item deleted successfully")
            self.assertEqual(result.status_code, 200)

    def test_admin_cannot_add_to_cart(self):
        """Tests that the admin cannot add items to the shopping cart"""
        with app.app_context():
            resp = self.client.post(
                "/api/v1/sales/cart",
                json=dict(
                    product_id=1,
                    quantity=2
                ),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.admin_token
                }
            )
            self.assertEqual(json.loads(resp.data).get(
                "msg"), "Attendants only")
            self.assertEqual(resp.status_code, 403)

    def test_attendant_cannot_get_all_sales_records(self):
        """
        Tests that a sales attendant cannot retrieved all sales records
        from the database
        """
        with app.app_context():
            response = self.client.post(
                "/api/v1/products/category",
                json=dict(category_name="Office Tables"),
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
                    product_name="OT5009",
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
            self.client.post(
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
            self.client.post(
                "/api/v1/sales",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.attendant_token
                }
            )
            result = self.client.get(
                "/api/v1/sales",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.attendant_token
                }
            )
            self.assertEqual(json.loads(result.data).get("msg"), "Admin previlidges required")
            self.assertEqual(result.status_code, 403)

    def test_get_single_sales_record(self):
        """Tests that a single sales record is retrieved from the database"""
        with app.app_context():
            response = self.client.post(
                "/api/v1/products/category",
                json=dict(category_name="Wall Units"),
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
                    product_name="WU-1900",
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
            self.client.post(
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
            result = self.client.post(
                "/api/v1/sales",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.attendant_token
                }
            )
            sales_id = json.loads(result.data).get("id")
            resp = self.client.get(
                "/api/v1/sales/{}".format(sales_id), 
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.admin_token
                }
            )
            self.assertEqual(json.loads(resp.data).get("msg"), "Success")
            self.assertEqual(resp.status_code, 200)

    def test_get_sales_for_specific_user(self):
        """Tests that sales records for a specific user are retrieved from the database"""
        with app.app_context():
            response = self.client.post(
                "/api/v1/products/category",
                json=dict(category_name="Office Chairs"),
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
                    product_name="OC-1900",
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
            self.client.post(
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
            self.client.post(
                "/api/v1/sales",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.attendant_token
                }
            )
            resp = self.client.get(
                "/api/v1/sales/user/{}".format(current_user.id), 
                headers={
                    "Content-Type": "application/json",
                    "Authorization": self.admin_token
                }
            )
            self.assertEqual(json.loads(resp.data).get("msg"), "Success")
            self.assertEqual(resp.status_code, 200)

    
