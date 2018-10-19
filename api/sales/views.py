from flask import request, jsonify

#  import product blueprint
from . import sales
#  import product controller
from . import dao
#  import validator
from api.validations import validate_product

controller = dao.SalesController()
validator = validate_product.ValidateProduct()


@sales.route("/sales/cart", methods=["POST"])
def add_to_cart():

    if request.method == "POST":
        result = validator.validate_input_data(request.form)
        if not result["is_true"]:
            return jsonify(result["errors"]), 400
        return controller.add_to_cart(request.form)


@sales.route("/sales/cart/items", methods=["GET"])
def get_cart_items():

    if request.method == "GET":
        return controller.get_cart_items()


@sales.route("/sales", methods=["POST"])
def add_sales_record():

    if request.method == "POST":
        return controller.add_sales_record()


@sales.route("/sales", methods=["GET"])
def get_all_sales_record():

    if request.method == "GET":
        return controller.get_all_sales_records()


@sales.route("/sales/<sales_id>", methods=["GET"])
def get_single_sales_record(sales_id):

    if request.method == "GET":
        return controller.get_single_sales_record(sales_id)
