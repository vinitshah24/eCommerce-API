from flask import request, jsonify, Blueprint
from flask_restful import Api, Resource

from api.users.models import DB, User
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

mod = Blueprint('users', __name__)
api = Api(mod)


class UserList(Resource):
    def get(self):
        users = User.query.all()
        output = []
        for user in users:
            user_data = {}
            user_data['public_id'] = user.public_id
            user_data['name'] = user.user_name
            # user_data['password'] = user.user_password
            user_data['admin'] = user.is_admin
            output.append(user_data)
        return jsonify({'users': output})


class UserCreate(Resource):
    def post(self):
        data = request.get_json()
        hashed_password = generate_password_hash(
            data['password'], method='sha256')
        user = User(
            public_id=str(uuid.uuid4()),
            user_name=data['name'],
            user_password=hashed_password,
            is_admin=False
        )
        DB.session.add(user)
        DB.session.commit()
        return jsonify({'message': 'User created successfully!'})


class UserActions(Resource):

    def get(self, public_id):
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            return jsonify({'message': 'User not found!'})
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.user_name
        # user_data['password'] = user.user_password
        user_data['admin'] = user.is_admin
        return jsonify({'user': user_data})

    def put(self, public_id):
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            return jsonify({'message': 'User not found!'})
        user.is_admin = True
        DB.session.commit()
        return jsonify({'message': 'User promoted to Admin!'})

    def delete(self, public_id):
        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            return jsonify({'message': 'User not found!'})
        DB.session.delete(user)
        DB.session.commit()
        return jsonify({'message': 'User deleted successfully'})


api.add_resource(UserList, '/users')
api.add_resource(UserCreate, '/user')
api.add_resource(UserActions, '/user/<public_id>')