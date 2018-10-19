from flask import request, jsonify

#  import user blueprint
from . import user
#  import authentication controller
from . import controllers
#  import data validator
from api.validations.validate_user import ValidateUserInput
validator = ValidateUserInput()
controller = controllers.AuthController()


@user.route("/user", methods=["POST"])
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
        if not result["is_true"]:
            return jsonify(result["errors"]), 400

        return controller.login_user(request.form)
