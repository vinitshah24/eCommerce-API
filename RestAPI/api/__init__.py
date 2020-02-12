from flask import Flask

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    from api.users.models import DB
    DB.init_app(app)

    # Blueprints
    from api.users.routes import mod
    app.register_blueprint(mod, url_prefix='/api/v1/')
    
    return app

"""
from flask import Flask
app = Flask(__name__)
from api.routes import mod
app.register_blueprint(api.routes.mod, url_prefix='/api')
"""