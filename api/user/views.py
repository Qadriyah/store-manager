from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

#  import user blueprint
from . import user
#  import authentication controller
from . import controllers
#  import data validator
from api.validations.validate_user import ValidateUserInput
from api.utils.jwt_helper import admin_required, user_loader_callback

validator = ValidateUserInput()
controller = controllers.AuthController()


@user.route("/user", methods=["POST"])
@admin_required
def register_user():

    if request.method == "POST":
        result = validator.validate_input_data(request.form)

        if not result["is_true"]:
            return jsonify(result["errors"]), 400
        return controller.register_user(request.form)


@user.route("/login", methods=["POST"])
def login_user():

    if request.method == "POST":
        result = validator.validate_login_input(request.form)
        print(result)
        return "good"
        if not result["is_true"]:
            return jsonify(result["errors"]), 400

        return controller.login_user(request.form)
