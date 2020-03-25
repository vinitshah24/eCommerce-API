""" Model for blacklisted tokens """

from api.extensions import DB


class TokenBlacklist(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    jti = DB.Column(DB.String(36), nullable=False)
    token_type = DB.Column(DB.String(10), nullable=False)
    user_identity = DB.Column(DB.String(50), nullable=False)
    revoked = DB.Column(DB.Boolean, nullable=False)
    expires = DB.Column(DB.DateTime, nullable=False)

    def to_dict(self):
        return {
            'token_id': self.id,
            'jti': self.jti,
            'token_type': self.token_type,
            'user_identity': self.user_identity,
            'revoked': self.revoked,
            'expires': self.expires
        }
