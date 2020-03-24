""" Register Blueprints """

from flask import Flask
from api.database import DB

from api.users.routes import users_model
from api.products.routes import products_model
from api.orders.routes import orders_model


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    DB.init_app(app)

    # Blueprints
    app.register_blueprint(users_model, url_prefix='/api/v1/')
    app.register_blueprint(products_model, url_prefix='/api/v1/')
    app.register_blueprint(orders_model, url_prefix='/api/v1/')
    return app
