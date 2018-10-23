from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

#  import product blueprint
from . import product
#  import product controller
from . import controllers
#  import validations
from api.validations import validate_product
from api.validations import validate_stock
from api.utils.jwt_helper import admin_required

controller = controllers.ProductController()
validator = validate_product.ValidateProduct()
stock_validator = validate_stock.ValidateStockInput()


@product.route("/products", methods=["POST"])
@admin_required
def add_product():
    """Add product route"""

    if request.method == "POST":
        result = validator.validate_input_data(request.form)
        if not result["is_true"]:
            return jsonify(result["errors"]), 400

        errors = validator.validate_number_fields(request.form)
        if not errors["is_true"]:
            return jsonify(errors["errors"]), 400

        return controller.add_product(request.form)


@product.route("/products", methods=["GET"])
@jwt_required
def get_all_products():
    """Get all products route"""

    if request.method == "GET":
        return controller.get_all_products()


@product.route("/products/<product_id>", methods=["GET"])
@jwt_required
def get_single_product(product_id):
    """Get a single product"""

    if request.method == "GET":
        return controller.get_single_product(product_id)


@product.route("/products/stock", methods=["POST"])
@admin_required
def add_stock():
    """Updates the stock level for a given product"""

    if request.method == "POST":
        result = stock_validator.validate_input_data(request.form)
        if not result["is_true"]:
            return jsonify(result["errors"]), 400

        return controller.add_stock(request.form)


@product.route("/products/delete/<product_id>", methods=["GET"])
@admin_required
def delete_product(product_id):
    """Deletes a product with a given product_id"""

    if request.method == "GET":
        return controller.delete_product(product_id)
