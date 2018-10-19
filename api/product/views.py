from flask import request, jsonify

#  import product blueprint
from . import product
#  import product controller
from . import controllers
#  import validations
from api.validations import validate_product

controller = controllers.ProductController()
validator = validate_product.ValidateProduct()


@product.route("/products", methods=["POST"])
def add_product():
    """Add product route"""

    if request.method == "POST":
        result = validator.validate_input_data(request.form)
        if not result["is_true"]:
            return jsonify(result["errors"]), 400
        return controller.add_product(request.form)


@product.route("/products", methods=["GET"])
def get_all_products():
    """Get all products route"""

    if request.method == "GET":
        return controller.get_all_products()


@product.route("/products/<product_id>", methods=["GET"])
def get_single_product(product_id):
    """Get a single product route"""

    if request.method == "GET":
        return controller.get_single_product(product_id)
