from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flasgger import swag_from

#  import sales blueprint
from . import sales
#  import sales controller
from . import controllers
#  import validator

from api.utils.jwt_helper import attendant_required, admin_required

controller = controllers.SalesController()


@sales.route("/sales/cart", methods=["POST"])
@attendant_required
@swag_from("../apidoc/sales/add_to_cart.yml")
def add_to_cart():
    if request.method == "POST":
        pass


@sales.route("/sales/cart/items", methods=["GET"])
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
