import os
from flask import Flask, request

from config import app_settings

app = Flask(__name__)
app.config.from_object(app_settings[os.environ.get("APP_ENV")])

#  Register blueprints
from .product import product as product_bp
app.register_blueprint(product_bp, url_prefix="/api/v1")

from .sales import sales as sales_bp
app.register_blueprint(sales_bp)
