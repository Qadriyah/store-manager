from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from flasgger import swag_from

#  import sales blueprint
from . import sales
#  import sales controller
from . import controllers

from api.validations.validation_tests import Validation
from api.utils.jwt_helper import attendant_required, admin_required
from api.validations.validation_schemas import stock_schema, date_schema, user_date_schema
from api import validator

controller = controllers.SalesController()
int_validator = Validation()


@sales.route("/sales/cart", methods=["POST"])
@attendant_required
@swag_from("../apidoc/sales/add_to_cart.yml")
def add_to_cart():
    if request.method == "POST":
        data = request.json
        err = validator.validate(data, stock_schema)
        if not err:
            return jsonify(validator.errors), 400
        return controller.add_to_cart(data)


@sales.route("/sales/cart", methods=["GET"])
@attendant_required
@swag_from("../apidoc/sales/get_cart_items.yml")
def get_cart_items():

    if request.method == "GET":
        return controller.get_cart_items()


@sales.route("/sales", methods=["POST"])
@attendant_required
@swag_from("../apidoc/sales/add_sales_order.yml")
def add_sales_record():

    if request.method == "POST":
        return controller.add_sales_record()


@sales.route("/sales/cart/delete/<cart_id>", methods=["DELETE"])
@attendant_required
@swag_from("../apidoc/sales/delete_cart_item.yml")
def delete_cart_item(cart_id):

    if request.method == "DELETE":
        if not int_validator.validate_integer(cart_id):
            return jsonify({"msg": "Id should be an integer"}), 401
        return controller.delete_cart_item(cart_id)


@sales.route("/sales", methods=["GET"])
@admin_required
@swag_from("../apidoc/sales/get_sales_records.yml")
def get_all_sales_record_():

    if request.method == "GET":
        return controller.get_all_sales_records({}, "all")


@sales.route("/sales/records", methods=["POST"])
@admin_required
@swag_from("../apidoc/sales/get_sales_records.yml")
def get_all_sales_record():

    if request.method == "POST":
        data = request.json
        err = validator.validate(data, date_schema)
        if not err:
            return jsonify(validator.errors), 400

        if not int_validator.validate_date(data.get("fro")) or not int_validator.validate_date(data.get("to")):
            return jsonify({"msg": "Wrong date"}), 401

        return controller.get_all_sales_records(data, "all")


@sales.route("/sales/<sales_id>", methods=["GET"])
@jwt_required
@swag_from("../apidoc/sales/get_sales_record_by_id.yml")
def get_single_sales_record(sales_id):

    if request.method == "GET":
        data = {"sales_id": int(sales_id)}
        if not int_validator.validate_integer(sales_id):
            return jsonify({"msg": "Id should be an integer"}), 401
        return controller.get_all_sales_records(data, "single")


@sales.route("/sales/user/<user_id>", methods=["POST"])
@jwt_required
@swag_from("../apidoc/sales/get_sales_record_by_user.yml")
def get_sales_for_attendant(user_id):

    if request.method == "POST":
        data = request.json
        err = validator.validate(data, user_date_schema)
        if not err:
            return jsonify(validator.errors), 400

        if not int_validator.validate_integer(user_id):
            return jsonify({"msg": "Id should be an integer"}), 401

        if not int_validator.validate_date(data.get("fro")) or not int_validator.validate_date(data.get("to")):
            return jsonify({"msg": "Wrong date"}), 401

        data.update({"user_id": int(user_id)})
        return controller.get_all_sales_records(data, "user")


@sales.route("/sales/user/<user_id>", methods=["GET"])
@jwt_required
@swag_from("../apidoc/sales/get_sales_record_by_user.yml")
def get_sales_for_attendant_(user_id):

    if request.method == "GET":
        if not int_validator.validate_integer(user_id):
            return jsonify({"msg": "Id should be an integer"}), 401

        return controller.get_user_sales_records(user_id)
