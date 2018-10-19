import os
import secrets
import json
from unittest import TestCase
from datetime import datetime
from flask import url_for

from api import app
from config import app_settings
from api.models.user import User
from api.user import controllers
from api.user import user
from api.validations import validate_user


class TestAuthentication(TestCase):
    def setUp(self):
        app.config.from_object(app_settings[os.environ.get("APP_ENV")])
        self.controller = controllers.AuthController()
        self.client = app.test_client()
        self.validator = validate_user.ValidateUserInput()
        self.user_input = dict(
            name="Baker Sekitoleko",
            username="Baker",
            password="mukungu",
            password2="mukungu"
        )

    def test_validate_user_input(self):
        """Tests that input fields are not empty"""
        result = self.validator.validate_input_data(self.user_input)
        self.assertTrue(result["is_true"])

    def test_register_user(self):
        """Tests that a user is registered successfully"""
        with app.app_context():
            res = self.controller.register_user(self.user_input)
            self.assertEqual(
                json.loads(res[0].data)["user"], "User registered successfully")

    def test_is_user_exists(self):
        """Tests that a user already exists"""
        with app.app_context():
            self.controller.register_user(self.user_input)
            self.assertTrue(self.controller.is_user_registered(
                self.user_input["username"]))

    def test_register_user_route(self):
        """Tests that the route registers a user"""
        with app.app_context():
            res = self.client.post("/api/v1/user", data=self.user_input)
            self.assertEqual(
                json.loads(res.data)["user"], "User registered successfully")
