""" Flask Main """

from flask import jsonify, make_response
from flask_jwt_extended import JWTManager
from api import create_app

app = create_app('config')

if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])
