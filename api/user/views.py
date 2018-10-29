from flask import request, jsonify, render_template
from flasgger import swag_from

#  import user blueprint
from . import user
#  import authentication controller
from . import controllers
#  import data validator
from api.validations.validate_user import ValidateUserInput
from api.utils.jwt_helper import admin_required
from api import app
from api import swagger

validator = ValidateUserInput()
controller = controllers.AuthController()


@user.route("/register", methods=["POST"])
@swag_from("../apidoc/user/register.yml")
@admin_required
def register_user():

    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        roles = request.form.get("roles")

        if not name or not username or not password or not password2 or not roles:
            return jsonify({"errors": "Server Erroe"}), 500

        errors = validator.validate_login_input(request.form)
        if not errors["is_true"]:
            return jsonify(errors["errors"]), 400

        result = validator.validate_input_data(request.form)
        if not result["is_true"]:
            return jsonify(result["errors"]), 400
        return controller.register_user(request.form)


@user.route("/login", methods=["POST"])
@swag_from("../apidoc/user/login_user.yml")
def login_user():

    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            return jsonify({"errors": "Server error"}), 500

        result = validator.validate_login_input(request.form)
        if not result["is_true"]:
            return jsonify(result["errors"]), 401
        return controller.login_user(request.form)


@app.route("/", methods=["GET"])
def welcome_page():
    return render_template(
        "welcome.html"
    )
