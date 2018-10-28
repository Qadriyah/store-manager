from flask import jsonify
from flask_jwt_extended import (
    create_access_token, get_jwt_identity, get_jwt_claims
)

from models.user import User
from api.sales.controllers import SalesController
from models.database import users
from api import bcrypt
from models.connection import Connection
from datetime import datetime


class AuthController:

    def __init__(self):
        conn = Connection()
        self.status_code = 200
        self.cursor = conn.connect()

    def register_user(self, request_data):
        """
        Registers and a new user

        Args:
            request_data(object): Request object holding form data

        Returns:
            tuple: With a response message and a status code
        """
        response = {}
        if self.__is_user_registered(request_data["username"]):
            response.update({"user": "User already exists"})
            self.status_code = 401
        else:
            #  Hash password
            password_hash = bcrypt.generate_password_hash(
                request_data["password"].strip(), 15)
            query = """
            INSERT INTO users(fullname, username, password, roles) \
            VALUES('{}', '{}', '{}', '{}')
            """.format(
                request_data["fullname"].strip(),
                request_data["username"].strip(),
                password_hash.decode(),
                request_data["roles"]
            )
            self.cursor.execute(query)
            response.update({"user": "User registered successfully"})
            self.status_code = 200

        return jsonify(response), self.status_code

    def __is_user_registered(self, username):
        """
        Checks if user already exists

        Args:
            username(str): Username provided by the user

        Returns:
            user(User): User if found, None otherwise
        """
        try:
            query = """
            SELECT id, fullname, username, password, roles \
            FROM users WHERE username = '{}'
            """.format(username)
            self.cursor.execute(query)
            result = self.cursor.fetchone()

        except Exception as error:
            print(error)
            return "Database error"
        return result

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
        user = self.__is_user_registered(request_data["username"])
        print(user)
        if not user:
            response.update({"errors": "Wrong username or password"})
            self.status_code = 401
        else:
            #  Check if password provided matches one in the database
            if bcrypt.check_password_hash(
                    "user.password", request_data["password"]):
                #  Create token
                token = create_access_token(
                    identity=user,
                    expires_delta=datetime.timedelta(days=7)
                )
                response.update({
                    "success": True,
                    "token": "Bearer {}".format(token)
                })
                self.status_code = 200
            else:
                response.update({"errors": "Wrong usrname or password"})
                self.status_code = 401

        return jsonify(response), self.status_code
