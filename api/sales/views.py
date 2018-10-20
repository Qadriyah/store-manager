from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

#  import sales blueprint
from . import sales
#  import sales controller
from . import controllers
#  import validator
from api.validations import validate_product
from api.utils.jwt_helper import attendant_required, admin_required

controller = controllers.SalesController()
validator = validate_product.ValidateProduct()


@sales.route("/sales/cart", methods=["POST"])
@attendant_required
def add_to_cart():

    if request.method == "POST":
        result = validator.validate_input_data(request.form)
        if not result["is_true"]:
            return jsonify(result["errors"]), 400
        return controller.add_to_cart(request.form)


@sales.route("/sales/cart/items", methods=["GET"])
@attendant_required
def get_cart_items():

    if request.method == "GET":
        return controller.get_cart_items()


@sales.route("/sales", methods=["POST"])
@attendant_required
def add_sales_record():

    if request.method == "POST":
        return controller.add_sales_record()


@sales.route("/sales", methods=["GET"])
@admin_required
def get_all_sales_record():

    if request.method == "GET":
        return controller.get_all_sales_records()


@sales.route("/sales/<sales_id>", methods=["GET"])
@jwt_required
def get_single_sales_record(sales_id):

    if request.method == "GET":
        return controller.get_single_sales_record(sales_id)
