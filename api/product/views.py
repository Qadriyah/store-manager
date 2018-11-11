from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flasgger import swag_from

#  import product blueprint
from . import product
#  import product controller
from . import controllers
from api.validations.validation_tests import Validation
from api.utils.jwt_helper import admin_required
from api.validations.validation_schemas import (
    product_schema, category_schema, stock_schema
)
from api import validator

controller = controllers.ProductController()
int_validator = Validation()


@product.route("/products", methods=["POST"])
@admin_required
@swag_from("../apidoc/product/add_product.yml")
def add_product():
    """Add product route"""

    if request.method == "POST":
        data = request.json
        err = validator.validate(data, product_schema)
        if not err:
            return jsonify(validator.errors), 400
        return controller.add_product(data)


@product.route("/products/category", methods=["POST"])
@admin_required
@swag_from("../apidoc/product/add_category.yml")
def add_category():
    if request.method == "POST":
        data = request.json
        err = validator.validate(data, category_schema)
        if not err:
            return jsonify(validator.errors), 400
        return controller.add_category(data)


@product.route("/products", methods=["GET"])
@jwt_required
@swag_from("../apidoc/product/get_products.yml")
def get_all_products():
    """Get all products route"""

    if request.method == "GET":
        return controller.get_all_products()


@product.route("/products/<product_id>", methods=["GET"])
@jwt_required
@swag_from("../apidoc/product/get_single_product.yml")
def get_single_product(product_id):
    """Get a single product"""

    if request.method == "GET":
        if not int_validator.validate_integer(product_id):
            return jsonify({"msg": "Product Id should be an integer"}), 400
        return controller.get_single_product(product_id)


@product.route("/products/stock", methods=["POST"])
@admin_required
@swag_from("../apidoc/product/add_stock.yml")
def add_stock():
    """Updates the stock level for a given product"""

    if request.method == "POST":
        data = request.json
        err = validator.validate(data, stock_schema)
        if not err:
            return jsonify(validator.errors), 400
        return controller.update_stock_level(data)


@product.route("/products/stock", methods=["GET"])
@admin_required
@swag_from("../apidoc/product/get_stock_items.yml")
def get_stock():
    """Gets a list of stock levels"""

    if request.method == "GET":
        return controller.get_stock()


@product.route("/products/delete/<product_id>", methods=["DELETE"])
@admin_required
@swag_from("../apidoc/product/delete_product.yml")
def delete_product(product_id):
    """Deletes a product with a given product_id"""

    if request.method == "DELETE":
        if not int_validator.validate_integer(product_id):
            return jsonify({"msg": "Product Id should be an integer"}), 400
        return controller.delete_product(product_id)


@product.route("/products/edit/<product_id>", methods=["PUT"])
@admin_required
@swag_from("../apidoc/product/edit_product.yml")
def edit_product(product_id):
    """Modifies the product details"""

    if request.method == "PUT":
        if not int_validator.validate_integer(product_id):
            return jsonify({"msg": "Product Id should be an integer"}), 400

        data = request.json
        err = validator.validate(data, product_schema)
        if not err:
            return jsonify(validator.errors), 400
        return controller.edit_product(product_id, data)


@product.route("/products/category", methods=["GET"])
@jwt_required
@swag_from("../apidoc/product/get_categories.yml")
def get_product_categories():
    """Modifies the product details"""

    if request.method == "GET":
        return controller.get_product_categories()


@product.route("/products/category/delete/<category_id>", methods=["DELETE"])
@admin_required
@swag_from("../apidoc/product/delete_category.yml")
def delete_product_category(category_id):
    if request.method == "DELETE":
        if not int_validator.validate_integer(category_id):
            return jsonify({"msg": "Category Id should be an integer"}), 400
        return controller.delete_product_category(category_id)


@product.route("/products/category/edit/<category_id>", methods=["PUT"])
@admin_required
@swag_from("../apidoc/product/edit_category.yml")
def edit_product_category(category_id):
    if request.method == "PUT":
        if not int_validator.validate_integer(category_id):
            return jsonify({"msg": "Category Id should be an integer"}), 400

        data = request.json
        err = validator.validate(data, category_schema)
        if not err:
            return jsonify(validator.errors), 400
        return controller.edit_product_category(category_id, data)
