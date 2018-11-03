import datetime
from flask import jsonify
from flask_jwt_extended import create_access_token, current_user

from models.models import User
from models.user import UserModels
from api import bcrypt


class AuthController:

    def __init__(self):
        self.status_code = 200
        self.user_models = UserModels()

    def register_user(self, data):
        """
        Registers and a new user

        Args:
            request_data(object): Request object holding form data

        Returns:
            tuple: With a response message and a status code
        """
        response = {}
        find_user = self.user_models.get_user(
            "username", data.get("username").strip())
        if find_user.get("msg") == "Found":
            response.update({"msg": "User already exists"})
            self.status_code = 401
        else:
            #  Hash password
            password_hash = bcrypt.generate_password_hash(
                data.get("password").strip(), 15)
            user = User(
                fullname=data.get("fullname").strip(),
                username=data.get("username").strip(),
                password=password_hash.decode(),
                roles=data.get("roles").strip()
            )
            result = self.user_models.add_user(user)
            if result.get("msg") == "Success":
                response.update({"msg": "User registered successfully"})
                self.status_code = 200
            else:
                response.update({"msg": result.get("msg")})
                self.status_code = 500

        return jsonify(response), self.status_code

    def login_user(self, data):
        """
        Authenticates a user and returns a JWT token back to the client if successful

        Args:
            request_data(object): Request object holding form data

        Returns:
            tuple: With a response message and a status code
        """
        response = {}
        #  Check if user exists
        user = self.user_models.get_user(
            "username", data.get("username").strip())
        if user.get("msg") == "User not found":
            response.update({"msg": "Wrong username"})
            self.status_code = 401
        else:
            #  Check if password provided matches one in the database
            if bcrypt.check_password_hash(user.get("user").get("password"),
                                          data.get("password")):
                #  Create token
                token = create_access_token(
                    identity=User(
                        id=user.get("user").get("id"),
                        fullname=user.get("user").get("fullname"),
                        username=user.get("user").get("username"),
                        roles=user.get("user").get("roles"),
                        created_at=user.get("user").get("created_at")
                    ),
                    expires_delta=datetime.timedelta(days=7)
                )
                response.update({
                    "success": True,
                    "token": token
                })
                self.status_code = 200
            else:
                response.update({"msg": "Wrong password"})
                self.status_code = 401

        return jsonify(response), self.status_code
