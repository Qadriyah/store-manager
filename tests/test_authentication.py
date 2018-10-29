import os
import json
from unittest import TestCase, skip

from api import app
from config.config import app_settings
from models.user import User
from api.user import controllers
from api.validations import validations
from models import connection


class TestAuthentication(TestCase):
    def setUp(self):
        conn = connection.Connection()
        #  app.config.from_object(app_settings[os.environ.get("APP_ENV")])
        self.controller = controllers.AuthController()
        self.client = app.test_client()
        self.validator = validations.ValidateInputData()
        self.cursor = conn.connect()
        #  Login as attendant to get the access token
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

    def tearDown(self):
        pass

    def test_user_login(self):
        """Tests that a user logins in successfully"""
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
        self.assertTrue(json.loads(res.data)["success"])
        self.assertEqual(res.status_code, 200)

    def test_wrong_username(self):
        """Tests that the username entered already exists"""
        res = self.client.post(
            "/api/v1/login",
            data=dict(
                username="Qadriyah",
                password="attendant"
            ),
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        self.assertEqual(json.loads(res.data)["errors"], "Wrong username")
        self.assertEqual(res.status_code, 401)

    def test_wrong_password(self):
        """Tests that the password entered is wrong"""
        res = self.client.post(
            "/api/v1/login",
            data=dict(
                username="attendant",
                password="mukungu"
            ),
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        self.assertEqual(json.loads(res.data)["errors"], "Wrong password")
        self.assertEqual(res.status_code, 401)

    @skip("Persistent data")
    def test_register_user(self):
        """Tests that a user is registered successfully"""
        res = self.client.post(
            "/api/v1/register",
            data=dict(
                fullname="Aretha Kebirungi",
                username="Aretha",
                password="programmer",
                password2="programmer",
                roles="attendant"
            ),
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": self.access_token
            }
        )
        self.assertEqual(json.loads(res.data)[
                         "msg"], "User registered successfully")
        self.assertEqual(res.status_code, 200)

    def test_user_already_exists(self):
        """Tests that the username entered already exists"""
        res = self.client.post(
            "/api/v1/register",
            data=dict(
                fullname="Aretha Kebirungi",
                username="Aretha",
                password="programmer",
                password2="programmer",
                roles="attendant"
            ),
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": self.access_token
            }
        )
        self.assertEqual(json.loads(res.data)["msg"], "User already exists")
        self.assertEqual(res.status_code, 401)

    def test_attendant_cannot_register_user(self):
        """Tests that the attendant cannot register a new user"""
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
        access_token_ = json.loads(res.data)["token"]
        response = self.client.post(
            "/api/v1/register",
            data=dict(
                fullname="Shirat Qadriyah",
                username="Qadie",
                password="smart",
                password2="smart",
                roles="attendant"
            ),
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": access_token_
            }
        )
        self.assertEqual(json.loads(response.data)[
                         "msg"], "Admin previlidges required")
        self.assertEqual(response.status_code, 403)
