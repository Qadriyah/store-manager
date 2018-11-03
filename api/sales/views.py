from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flasgger import swag_from
import secrets

#  import sales blueprint
from . import sales
#  import sales controller
from . import controllers

from api.utils.jwt_helper import attendant_required, admin_required
from api.validations.validation_schemas import (
    cart_schema, sales_schema
)
from api import validator

controller = controllers.SalesController()


@sales.route("/sales/cart", methods=["POST"])
@attendant_required
@swag_from("../apidoc/sales/add_to_cart.yml")
def add_to_cart():
    if request.method == "POST":
        data = request.json
        err = validator.validate(data, cart_schema)
        if not err:
            return jsonify(validator.errors)
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
        cart_items = controller.get_cart_items()
        return controller.add_sales_record(cart_items[0])


@sales.route("/sales/cart/delete/<cid>/<pid>/<qty>", methods=["DELETE"])
@attendant_required
def delete_cart_item(cid, pid, qty):

    if request.method == "DELETE":
        return controller.delete_cart_item(cid, pid, qty)


@sales.route("/sales", methods=["GET"])
@admin_required
@swag_from("../apidoc/sales/get_sales_records.yml")
def get_all_sales_record():

    if request.method == "GET":
        return controller.get_all_sales_records()


@sales.route("/sales/<sales_id>", methods=["GET"])
@jwt_required
@swag_from("../apidoc/sales/get_single_sales_record.yml")
def get_single_sales_record(sales_id):

    if request.method == "GET":
        return controller.get_single_sales_record(sales_id)


@sales.route("/sales/user/<user_id>", methods=["GET"])
@jwt_required
@swag_from("../apidoc/sales/get_single_sales_record.yml")
def get_sales_for_attendant(user_id):

    if request.method == "GET":
        return controller.get_sales_for_attendant(user_id)
