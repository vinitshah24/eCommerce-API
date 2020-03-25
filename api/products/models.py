""" Model for products table """

from api.extensions import DB


class Products(DB.Model):
    """ products table """
    __tablename__ = 'products'
    id = DB.Column(DB.Integer, primary_key=True)
    public_id = DB.Column(DB.String(50), unique=True, nullable=False)
    name = DB.Column(DB.String(50), nullable=False)
    company = DB.Column(DB.String(50), nullable=False, default="unbranded ")
    description = DB.Column(DB.String(50), nullable=False)
    category = DB.Column(DB.String(50), nullable=False)
    cost = DB.Column(DB.Float, nullable=False)
