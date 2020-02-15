from api.database import DB


class User(DB.Model):
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, primary_key=True)
    public_id = DB.Column(DB.String(50), unique=True, nullable=False)
    username = DB.Column(DB.String(50), nullable=False)
    password = DB.Column(DB.String(80), nullable=False)
    is_admin = DB.Column(DB.Boolean)
