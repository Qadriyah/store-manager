import os
import json
from unittest import TestCase, skip

from api import app
from models.models import User
from models.user import UserModels
from models.database_objects import DatabaseObjects
from config.config import app_settings


class TestUserModels(TestCase):
    def setUp(self):
        app.config.from_object(app_settings[os.environ.get("APP_ENV")])
        self.db_objects = DatabaseObjects()
        self.user_models = UserModels()

    def tearDown(self):
        self.db_objects.delete_database_tables()

    def test_add_user(self):
        """Tests that a user is added successfully"""
        with app.app_context():
            user = User(
                fullname="Mukungu Baker",
                username="Becks",
                password="andela",
                roles="attendant"
            )
            result = self.user_models.add_user(user)
            self.assertEqual(result.get("msg"), "Success")

    def test_add_user_failure(self):
        """Tests that a user failed to add to the database"""
        with app.app_context():
            result = self.user_models.add_user({})
            self.assertEqual(result.get("msg"), "Some fields were missing")

    def test_get_user(self):
        """Tests that a single user is retrieved from the database"""
        with app.app_context():
            result = self.user_models.get_user("username", "admin")
            self.assertEqual(result.get("msg"), "Found")

    def test_get_user_failure(self):
        """Tests that get user failed with errors"""
        with app.app_context():
            result = self.user_models.get_user("data", "data")
            self.assertEqual(result.get("msg"), "Unknown column data")

    def test_get_all_users(self):
        """Tests that all users are retrieved from the database"""
        with app.app_context():
            result = self.user_models.get_all_users()
            self.assertEqual(result.get("msg"), "Found")
