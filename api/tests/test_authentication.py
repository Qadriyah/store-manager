import os
import secrets
import json
from unittest import TestCase
from datetime import datetime

from api import app
from config import app_settings
from api.models.user import User
from api.user import user, controllers
from api.validations import validate_user


class TestAuthentication(TestCase):
    def setUp(self):
        app.config.from_object(app_settings[os.environ.get("APP_ENV")])
        self.controller = controllers.AuthController()
        self.client = app.test_client()
        self.validator = validate_user.ValidateUserInput()
        self.user1 = dict(
            name="John Doe",
            username="Jones",
            password="mukungu",
            password2="mukungu",
            roles="attendant"
        )
        self.user2 = dict(
            name="Loren Ipsum",
            username="Loren",
            password="testing",
            password2="testing",
            roles="attendant"
        )
        #  Login as attendant to get the access token
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
        self.access_token_ = json.loads(response.data)["token"]

    def test_validate_user_input(self):
        """Tests that input fields are not empty"""
        result = self.validator.validate_input_data(self.user1)
        self.assertTrue(result["is_true"])

    def test_register_user(self):
        """Tests that a user is registered successfully"""
        with app.app_context():
            res = self.controller.register_user(self.user1)
            self.assertEqual(
                json.loads(res[0].data)["user"], "User registered successfully")

    def test_is_user_exists(self):
        """Tests that a user already exists"""
        with app.app_context():
            self.assertTrue(self.controller.is_user_registered("admin"))

    def test_register_user_route(self):
        """Tests that the route registers a user"""
        with app.app_context():
            #  Login to get the access token
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
            access_token = json.loads(response.data)["token"]
            #  Register new user
            res = self.client.post(
                "/api/v1/register",
                data=self.user2,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": access_token
                }
            )
            self.assertEqual(
                json.loads(res.data)["user"], "User registered successfully")

    def test_validate_login_input(self):
        """Tests that input fields are not empty"""
        result = self.validator.validate_input_data(self.user1)
        self.assertTrue(result["is_true"])

    def test_login_user(self):
        """Tests that a user receives a JWT token for a successful login"""
        with app.app_context():
            res = self.controller.login_user(dict(
                username="admin",
                password="admin"
            ))
            self.assertTrue(json.loads(res[0].data)["success"])

    def test_login_user_route(self):
        """
        Tests that the route authenticates a user and returns a JWT
        token that shall be used for further requests
        """
        with app.app_context():
            res = self.client.post(
                "/api/v1/login",
                data=dict(
                    username="admin",
                    password="admin"
                ),
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            )
            self.assertTrue(json.loads(res.data)["success"])

    def test_attendant_cannot_add_account(self):
        """Tests that the attendant cannot add a new user account"""
        with app.app_context():
            res = self.client.post(
                "/api/v1/register",
                data=self.user2,
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": self.access_token_
                }
            )
            self.assertEqual(
                json.loads(res.data)["msg"], "Admin previlidges required")

    