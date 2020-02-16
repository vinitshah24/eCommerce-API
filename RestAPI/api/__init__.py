""" Register Blueprints """

from flask import Flask
from api.database import DB

from api.users.routes import mod


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    DB.init_app(app)  # SQLAlchemy

    # Blueprints
    app.register_blueprint(mod, url_prefix='/api/v1/')

    return app
