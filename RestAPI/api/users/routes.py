from flask import request, jsonify, Blueprint
from api.users.models import DB, User
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

mod = Blueprint('users', __name__)

@mod.route('/users', methods=['GET'])
def get_all_users():
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


@mod.route('/user/<public_id>', methods=['GET'])
def get_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'User not found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.user_name
    # user_data['password'] = user.user_password
    user_data['admin'] = user.is_admin

    return jsonify({'user': user_data})


@mod.route('/user/add/', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    user = User(
        public_id=str(uuid.uuid4()),
        user_name=data['name'],
        user_password=hashed_password,
        is_admin=False
    )
    DB.session.add(user)
    DB.session.commit()

    return jsonify({'message': 'User created successfully!'})


@mod.route('/user/promote/<public_id>', methods=['PUT'])
def promote_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'User not found!'})

    user.is_admin = True
    DB.session.commit()
    return jsonify({'message': 'User promoted to Admin!'})


@mod.route('/user/delete/<public_id>', methods=['DELETE'])
def delete_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message': 'User not found!'})

    DB.session.delete(user)
    DB.session.commit()

    return jsonify({'message': 'User deleted successfully'})
