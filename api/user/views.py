from flask import request, jsonify, render_template
from flasgger import swag_from

#  import user blueprint
from . import user
#  import authentication controller
from . import controllers
#  import data validator
from api.validations.validations import ValidateInputData
from api.utils.jwt_helper import admin_required
from api import app
from api import swagger

validator = ValidateInputData()
controller = controllers.AuthController()


@user.route("/register", methods=["POST"])
@swag_from("../apidoc/user/register.yml")
@admin_required
def register_user():

    if request.method == "POST":
        errors = {}
        if not validator.validate_user_data(request.form):
            errors.update({"msg": "All fields are required"})
            return jsonify(errors), 401

        if not validator.validate_password_match(request.form):
            errors.update({"msg": "Passwords dont match"})
            return jsonify(errors), 401

        return controller.register_user(request.form)


@user.route("/login", methods=["POST"])
@swag_from("../apidoc/user/login_user.yml")
def login_user():

    if request.method == "POST":
        errors = {}
        username = validator.validate_text_fields(request.form["username"])
        password = validator.validate_text_fields(request.form["password"])
        if not username or not password:
            errors.update({"msg": "Wrong username or password"})
            return jsonify(errors), 401

        return controller.login_user(request.form)


@app.route("/", methods=["GET"])
def welcome_page():
    return render_template(
        "welcome.html"
    )
