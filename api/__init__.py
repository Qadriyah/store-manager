import os
from flask import Flask, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_script import Manager
from cerberus import Validator

from config.config import app_settings
from models.database_objects import DatabaseObjects
from models.delete import Delete
from models.insert import Insert
from models.update import Update
from models.select import Select

app = Flask(__name__)
app.config.from_object(app_settings[os.environ.get("APP_ENV")])
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
Swagger(app)
manager = Manager(app)
validator = Validator()
connection = DatabaseObjects()
delete = Delete(connection)
insert = Insert(connection)
update = Update(connection)
select = Select(connection)

#  Register blueprints
from .product import product as product_bp
app.register_blueprint(product_bp, url_prefix="/api/v1")

from .sales import sales as sales_bp
app.register_blueprint(sales_bp, url_prefix="/api/v1")

from .user import user as user_bp
app.register_blueprint(user_bp, url_prefix="/api/v1")


@app.before_first_request
def delete_expired_tokens():
    delete.delete_expired_tokens()
