from flask import request, jsonify
from flasgger import swag_from

#  import user blueprint
from . import user

from . import controllers
from api.utils.jwt_helper import admin_required
from flask_jwt_extended import get_raw_jwt, jwt_required
from api.validations.validation_schemas import (
    login_schema, register_schema
)
from api import validator

controller = controllers.AuthController()


@user.route("/register", methods=["POST"])
@swag_from("../apidoc/user/register.yml")
@admin_required
def register_user():

    if request.method == "POST":
        data = request.json
        err = validator.validate(data, register_schema)
        if not err:
            return jsonify(validator.errors), 400

        return controller.register_user(data)


@user.route("/login", methods=["POST"])
@swag_from("../apidoc/user/login_user.yml")
def login_user():

    if request.method == "POST":
        data = request.json
        err = validator.validate(data, login_schema)
        if not err:
            return jsonify(validator.errors), 400

        return controller.login_user(data)


@user.route("/logout", methods=["DELETE"])
@jwt_required
def logout():
    token = get_raw_jwt()
    return controller.logout(token.get("jti"))


@user.route("/users", methods=["GET"])
@admin_required
def get_users():
    return controller.get_all_users('all')


@user.route("/attendants", methods=["GET"])
@jwt_required
def get_sales_attendants():
    return controller.get_all_users('attendant')
