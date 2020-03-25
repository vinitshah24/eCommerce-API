""" Binding Flask SQLAlchemy and JWT """

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

DB = SQLAlchemy()
jwt = JWTManager()
