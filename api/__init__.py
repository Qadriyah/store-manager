import os
from flask import Flask, request

from config import app_settings

app = Flask(__name__)

if os.environ.get("APP_ENV") == "development":
    app.config.from_object(app_settings["development"])

if os.environ.get("APP_ENV") == "testing":
    app.config.from_object(app_settings["testing"])

if os.environ.get("APP_ENV") == "production":
    app.config.from_object(app_settings["production"])

#  Register blueprints
from .product import product as product_bp
app.register_blueprint(product_bp)

from .sales import sales as sales_bp
app.register_blueprint(sales_bp)