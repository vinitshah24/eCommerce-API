from api.database import DB


class User(DB.Model):
    user_id = DB.Column(DB.Integer, primary_key=True)
    public_id = DB.Column(DB.String(50), unique=True)
    user_name = DB.Column(DB.String(50))
    user_password = DB.Column(DB.String(80))
    is_admin = DB.Column(DB.Boolean)
