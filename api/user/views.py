from flask import request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

#  import user blueprint
from . import user
#  import authentication controller
from . import controllers
#  import data validator
from api.validations.validate_user import ValidateUserInput
from api.utils.jwt_helper import admin_required, user_loader_callback
from api import app

validator = ValidateUserInput()
controller = controllers.AuthController()


@user.route("/register", methods=["POST"])
@admin_required
def register_user():

    if request.method == "POST":
        result = validator.validate_input_data(request.form)
        if not result["is_true"]:
            return jsonify(result["errors"]), 400

        errors = validator.validate_login_input(request.form)
        if not errors["is_true"]:
            return jsonify(errors["errors"]), 400
        return controller.register_user(request.form)


@user.route("/login", methods=["POST"])
def login_user():

    if request.method == "POST":
        result = validator.validate_login_input(request.form)
        if not result["is_true"]:
            return jsonify(result["errors"]), 400
        return controller.login_user(request.form)


@app.route("/", methods=["GET"])
def welcome_page():
    return render_template(
        "welcome.html"
    )
