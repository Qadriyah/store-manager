from flask import request, jsonify

#  import product blueprint
from . import product
#  import product controller
from . import dao
#  import validations
from api.validations import validate_product

controller = dao.ProductController()
validator = validate_product.ValidateProduct()


@product.route("/products", methods=["POST"])
def add_product():
    """Add product route"""
    if request.method == "POST":
        result = validator.validate_input_data(request.form)
        if not result["is_true"]:
            return jsonify(result["errors"]), 400
        return controller.add_product(request.form)
