import os
import json
from unittest import TestCase

from api import app
from models.database_objects import DatabaseObjects
from api.user import controllers
from config.config import app_settings


class TestAuthentication(TestCase):
    def setUp(self):
        app.config.from_object(app_settings[os.environ.get("APP_ENV")])
        self.db_objects = DatabaseObjects()
        self.controller = controllers.AuthController()
        self.client = app.test_client()
        #  Login as admin to get the access token
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

    def test_user_login(self):
        """Tests that a user logins in successfully"""
        data = dict(
            username="admin",
            password="admin"
        )
        res = self.client.post(
            "/api/v1/login",
            json=data,
            headers={
                "Content-Type": "application/json"
            }
        )
        self.assertTrue(json.loads(res.data)["success"])
        self.assertEqual(res.status_code, 200)

    def test_wrong_username(self):
        """Tests that the username entered already exists"""
        data = dict(
            username="Qadriyah",
            password="admin"
        )
        res = self.client.post(
            "/api/v1/login",
            json=data,
            headers={
                "Content-Type": "application/json"
            }
        )
        self.assertEqual(json.loads(res.data)["msg"], "Username not found")
        self.assertEqual(res.status_code, 404)

    def test_wrong_password(self):
        """Tests that the password entered is wrong"""
        data = dict(
            username="admin",
            password="mukungu"
        )
        res = self.client.post(
            "/api/v1/login",
            json=data,
            headers={
                "Content-Type": "application/json"
            }
        )
        self.assertEqual(json.loads(res.data)["msg"], "Wrong password")
        self.assertEqual(res.status_code, 401)

    def test_register_user(self):
        """Tests that a user is registered successfully"""
        data = dict(
            fullname="Aretha Kebirungi",
            username="Aretha",
            password="programmer",
            password2="programmer",
            roles="attendant"
        )
        res = self.client.post(
            "/api/v1/register",
            json=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": self.access_token
            }
        )
        self.assertEqual(json.loads(res.data)["msg"], "Success")
        self.assertEqual(res.status_code, 200)

    def test_user_already_exists(self):
        """Tests that the username entered already exists"""
        data = dict(
            fullname="Aretha Kebirungi",
            username="admin",
            password="programmer",
            password2="programmer",
            roles="attendant"
        )
        res = self.client.post(
            "/api/v1/register",
            json=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": self.access_token
            }
        )
        self.assertEqual(json.loads(res.data)["msg"], "User already exists")
        self.assertEqual(res.status_code, 401)

    def test_attendant_cannot_register_user(self):
        """Tests that the attendant cannot register a new user"""
        data = dict(
            fullname="Henry Bulemi",
            username="Henry",
            password="attendant",
            password2="attendant",
            roles="attendant"
        )
        self.client.post(
            "/api/v1/register",
            json=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": self.access_token
            }
        )
        data1 = dict(
            username="Henry",
            password="attendant"
        )
        res = self.client.post(
            "/api/v1/login",
            json=data1,
            headers={
                "Content-Type": "application/json"
            }
        )
        access_token_ = "Bearer {}".format(json.loads(res.data)["token"])
        data2 = dict(
            fullname="Shirat Qadriyah",
            username="Qadie",
            password="smart",
            password2="smart",
            roles="attendant"
        )
        response = self.client.post(
            "/api/v1/register",
            json=data2,
            headers={
                "Content-Type": "application/json",
                "Authorization": access_token_
            }
        )
        self.assertEqual(json.loads(response.data)[
                         "msg"], "Admin previlidges required")
        self.assertEqual(response.status_code, 403)
