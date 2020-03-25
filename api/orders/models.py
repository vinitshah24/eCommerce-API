""" Model for orders table """

from api.extensions import DB


class Orders(DB.Model):
    """ orders table """
    __tablename__ = 'orders'
    id = DB.Column(DB.Integer,  primary_key=True)
    public_id = DB.Column(DB.String(50), unique=True, nullable=False)
    user_public_id = DB.Column(DB.String(50),
                               DB.ForeignKey('users.public_id'),
                               unique=True, nullable=False)
    product_public_id = DB.Column(DB.String(50),
                                  DB.ForeignKey('products.public_id'),
                                  unique=True, nullable=False)
