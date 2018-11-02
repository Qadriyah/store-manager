from flask import request, jsonify, render_template
from flasgger import swag_from

#  import user blueprint
from . import user

from . import controllers
from api.utils.jwt_helper import admin_required
from api import app, Swagger
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


@app.route("/", methods=["GET"])
def welcome_page():
    return render_template(
        "welcome.html"
    )
