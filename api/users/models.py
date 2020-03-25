""" Model for users table """

from api.extensions import DB


class Users(DB.Model):
    """ users table """
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, primary_key=True)
    public_id = DB.Column(DB.String(50), unique=True, nullable=False)
    first_name = DB.Column(DB.String(50), nullable=False)
    last_name = DB.Column(DB.String(50), nullable=False)
    email = DB.Column(DB.String(60))
    username = DB.Column(DB.String(50), nullable=False)
    password = DB.Column(DB.String(80), nullable=False)
    is_admin = DB.Column(DB.Boolean)
