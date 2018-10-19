import secrets
import datetime
from flask import jsonify
from flask_jwt_extended import create_access_token

from api import app
from api.models.user import User
from api.sales.controllers import SalesController
from api import bcrypt
from api import jwt


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
                password=password_hash,
                user_type="admin"
            )
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
            user(User): User if found, None otherwise
        """
        if SalesController().is_table_empty(self.users):
            return None

        for user in self.users:
            if user.username == username:
                return user

    def login_user(self, request_data):
        """
        Authenticates a user and returns a JWT token back to the client if successful

        Args:
            request_data(object): Request object holding form data

        Returns:
            tuple: With a response message and a status code
        """
        response = {}
        #  Check if user exists
        result = self.is_user_registered(request_data["username"])
        if not result:
            response.update({"errors": "Wrong username or password"})
            self.status_code = 401
        else:
            #  Check if password provided matches one in the database
            if bcrypt.check_password_hash(
                    result.password, request_data["password"]):
                #  Create jwt payload
                jwt_payload = {
                    "id": result.id,
                    "name": result.name,
                    "username": result.username
                }
                #  Create token
                token = create_access_token(
                    jwt_payload, expires_delta=datetime.timedelta(days=7))
                response.update({
                    "success": True,
                    "token": "Bearer {}".format(token)
                })
                self.status_code = 200
            else:
                response.update({"error": "Wrong email or password"})
                self.status_code = 401

        return jsonify(response), self.status_code
