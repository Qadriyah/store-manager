import secrets
from flask import jsonify
from flask_jwt_extended import create_access_token

from api import app
from api.models.user import User
from api.sales.dao import SalesController
from api import bcrypt


class AuthController:

    def __init__(self):
        self.status_code = 200
        self.users = []

    def register_user(self, request_data):
        """
        Registers and a new user

        Args:
            request_data(object): Request object holding form data

        Returns:
            tuple: With a response message and a status code
        """
        response = {}
        if self.is_user_registered(request_data["username"]):
            response.update({"user": "User already exists"})
            self.status_code = 401
        else:
            #  Hash password
            password_hash = bcrypt.generate_password_hash(
                request_data["password"], 15)
            new_user = User(
                id=secrets.token_hex(4),
                name=request_data["name"],
                username=request_data["username"],
                password=password_hash
            )
            print(new_user)
            self.users.append(new_user)
            response.update({"user": "User registered successfully"})
            self.status_code = 200

        return jsonify(response), self.status_code

    def is_user_registered(self, username):
        """
        Checks if user already exists

        Args:
            username(str): Username provided by the user

        Returns:
            bool: True if found, False otherwise
        """
        found = False
        if SalesController().is_table_empty(self.users):
            return found

        for user in self.users:
            if user.username == username:
                found = True
                break
        return found
