import datetime
from flask import jsonify
from flask_jwt_extended import create_access_token, decode_token

from models.models import User
from api import bcrypt, app, select, insert, update


class AuthController:

    def __init__(self):
        self.status_code = 200

    def register_user(self, data):
        """
        Registers and a new user
        """
        response = {}
        user = select.select_all_records(
            ["username"], "users", where="username",
            cell=data.get("username").strip(), order="username", sort="ASC")

        if user.get("msg") == "Found":
            response.update({"msg": "User already exists"})
            self.status_code = 401
        else:
            #  Hash password
            password_hash = bcrypt.generate_password_hash(
                data.get("password").strip(), 15)
            data["password"] = password_hash.decode()
            response = insert.insert_user(data)

            if response.get("msg") == "Success":
                self.status_code = 200
            else:
                self.status_code = 500

        return jsonify(response), self.status_code

    def get_all_users(self, role):
        """Retrieves a list of all users"""
        response = {}
        query = """
        SELECT id, fullname, username, roles, created_at \
        FROM users WHERE status = '{}' ORDER BY fullname ASC
        """.format('Active')

        if role != "all":
            query = """
            SELECT id, fullname, username, roles, created_at \
            FROM users WHERE status = '{}' AND roles = '{}' ORDER BY fullname ASC
            """.format('Active', role)

        response = select.select_from_users(query)
        if response.get("msg") == "Empty":
            self.status_code = 404

        if response.get("msg") == "Success":
            self.status_code = 200

        if response.get("msg") == "Failure":
            self.status_code = 500

        return jsonify(response), self.status_code

    def get_single_user(self, user_id):
        """Retrieves a single user using the userId"""
        response = {}
        query = """
        SELECT id, fullname, username, roles, created_at FROM users WHERE id = {}
        """.format(user_id)

        response = select.select_from_users(query)
        if response.get("msg") == "Empty":
            self.status_code = 404

        if response.get("msg") == "Success":
            self.status_code = 200

        if response.get("msg") == "Failure":
            self.status_code = 500

        return jsonify(response), self.status_code

    def login_user(self, data):
        """
        Authenticates a user and returns a JWT token back to the client if successful
        """
        response = {}
        #  Check if user exists
        columns = ["id", "fullname", "username",
                   "password", "roles", "created_at"]
        user = select.select_all_records(
            columns, "users", where="username",
            cell=data.get("username").strip(), order="username", sort="ASC")

        if user.get("msg") == "Empty":
            response.update({"msg": "Username not found"})
            self.status_code = 404
        else:
            #  Check if password provided matches one in the database
            if bcrypt.check_password_hash(user.get("users")[0].get("password"),
                                          data.get("password")):
                #  Create token
                token = create_access_token(
                    identity=User(
                        id=user.get("users")[0].get("id"),
                        fullname=user.get("users")[0].get("fullname"),
                        username=user.get("users")[0].get("username"),
                        roles=user.get("users")[0].get("roles"),
                        created_at=user.get("users")[0].get("created_at")
                    ),
                    expires_delta=datetime.timedelta(days=7)
                )
                response.update({
                    "success": True,
                    "token": token
                })
                self.status_code = 200
                insert.insert_blacklist(self.decode_jwt_token(token))
            else:
                response.update({"msg": "Wrong password"})
                self.status_code = 401

        return jsonify(response), self.status_code

    def logout(self, jti):
        """Logs out a user"""
        response = update.update_token(jti)
        if response.get("msg") == "Success":
            self.status_code = 200
        else:
            self.status_code = 500

        return jsonify(response), self.status_code

    def decode_jwt_token(self, token):
        """Decodes the JWT token"""
        payload = decode_token(token)

        return payload
