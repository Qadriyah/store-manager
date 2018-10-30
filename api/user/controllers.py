import datetime
from flask import jsonify
from flask_jwt_extended import create_access_token, current_user

from models.models import User
from api import bcrypt, connection
from models.connection import Connection


class AuthController:

    def __init__(self):
        self.status_code = 200
        self.cursor = connection.cursor

    def register_user(self, request_data):
        """
        Registers and a new user

        Args:
            request_data(object): Request object holding form data

        Returns:
            tuple: With a response message and a status code
        """
        response = {}
        if self.get_user(request_data["username"], self.cursor):
            response.update({"msg": "User already exists"})
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
            response.update({"msg": "User registered successfully"})
            self.status_code = 200

        return jsonify(response), self.status_code

    @classmethod
    def get_user(cls, username, cursor):
        """
        Checks if user already exists

        Args:
            username(str): Username provided by the user

        Returns:
            user(User): User if found, None otherwise
        """
        try:
            query = """
            SELECT id, fullname, username, password, roles, created_at \
            FROM users WHERE username = '{}'
            """.format(username)
            cursor.execute(query)
            result = cursor.fetchone()
            if not result:
                return None

        except Exception as error:
            print(error)
            return "Database error"
        return User(
            id=result["id"],
            fullname=result["fullname"],
            username=result["username"],
            password=result["password"],
            roles=result["roles"],
            created_at=result["created_at"]
        )

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
        user = self.get_user(request_data["username"], self.cursor)
        if not user:
            response.update({"errors": "Wrong username"})
            self.status_code = 401
        else:
            #  Check if password provided matches one in the database
            if bcrypt.check_password_hash(
                    user.password, request_data["password"]):
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
                response.update({"errors": "Wrong password"})
                self.status_code = 401

        return jsonify(response), self.status_code
