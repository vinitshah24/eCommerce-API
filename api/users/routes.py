""" Routes for user """

import uuid
from flask import request, jsonify, Blueprint, make_response
from flask import current_app as app
from flask_restful import Api, Resource
from flask_jwt_extended import (
    jwt_required,
    jwt_optional,
    get_jwt_identity,
    jwt_refresh_token_required,
    fresh_jwt_required,
    get_raw_jwt,
    create_access_token,
    create_refresh_token,
)
from werkzeug.security import safe_str_cmp
from api.users.models import DB, Users
import api.security.jwt
from api.security.models import DB, TokenBlacklist
from api.security.blacklist_helpers import (
    is_token_revoked, add_token_to_database, get_user_tokens,
    revoke_token, unrevoke_token,
    prune_database
)

users_model = Blueprint('users', __name__)
api_login = Api(users_model)


class UserList(Resource):
    @jwt_required  # Will require accesss token
    @jwt_optional  # Using jwt to check public_key for isAdmin value
    def get(self):
        """Get the list of users"""
        jwt_public_id = get_jwt_identity()
        data = Users.query.filter_by(public_id=jwt_public_id).first()
        if data.is_admin:
            users = Users.query.all()
            output = []
            for user in users:
                user_data = {}
                user_data['public_id'] = user.public_id
                user_data['first_name'] = user.first_name
                user_data['last_name'] = user.last_name
                user_data['email'] = user.email
                user_data['username'] = user.username
                # user_data['password'] = user.password
                user_data['admin'] = user.is_admin
                output.append(user_data)
            return jsonify({'users': output})
        return make_response(jsonify({'message': 'Unauthorized request!'}), 401)


class UserActions(Resource):
    def post(self):
        """ Create a new user """
        data = request.get_json()
        user = Users(
            public_id=str(uuid.uuid4()),
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            username=data['username'],
            password=data['password'],
            is_admin=False
        )
        DB.session.add(user)
        DB.session.commit()
        return make_response(jsonify({'message': 'User created successfully!'}), 200)

    @jwt_required  # Will require accesss token
    def get(self):
        """ Get user details """
        public_id = get_jwt_identity()
        print(public_id)
        user = Users.query.filter_by(public_id=public_id).first()
        if not user:
            return make_response(jsonify({'message': 'User not found!'}), 401)
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['first_name'] = user.first_name
        user_data['last_name'] = user.last_name
        user_data['email'] = user.email
        user_data['username'] = user.username
        user_data['admin'] = user.is_admin
        return make_response(jsonify({'user': user_data}), 200)

    @jwt_required  # Will require accesss token
    def put(self):
        """ Escalate user privileges to admin """
        public_id = get_jwt_identity()
        print(public_id)
        user = Users.query.filter_by(public_id=public_id).first()
        if not user:
            return make_response(jsonify({'message': 'User not found!'}), 401)
        user.is_admin = True
        DB.session.commit()
        return make_response(jsonify({'message': 'User promoted to Admin!'}), 200)

    # Will require a fresh token [re-login] to ensure the user is authentic
    @fresh_jwt_required
    def delete(self):
        """ Remove a user """
        public_id = get_jwt_identity()
        user = Users.query.filter_by(public_id=public_id).first()
        if not user:
            return make_response(jsonify({'message': 'User not found!'}), 401)
        DB.session.delete(user)
        DB.session.commit()
        return make_response(jsonify({'message': 'User deleted successfully'}), 200)


class ChangeEmail(Resource):
    @jwt_required  # Will require accesss token
    def put(self, email):
        """ Change Email """
        public_id = get_jwt_identity()
        user = Users.query.filter_by(public_id=public_id).first()
        user.email = email
        DB.session.commit()
        return make_response(jsonify({'message': 'Email updated successfully'}), 200)


class UserLogin(Resource):
    def post(self):
        """ User Login """
        json_data = request.get_json()
        input_user = json_data['username']
        input_password = json_data['password']
        data = Users.query.filter_by(username=input_user).first()
        if data is None:
            return make_response(jsonify({'message': 'Invalid Credentials!'}), 401)
        elif safe_str_cmp(data.username, input_user) and safe_str_cmp(data.password, input_password):
            access_token = create_access_token(
                identity=data.public_id, fresh=True)
            refresh_token = create_refresh_token(data.public_id)
            # Store the tokens in our store with a status of not currently revoked.
            add_token_to_database(
                access_token, app.config['JWT_IDENTITY_CLAIM'])
            add_token_to_database(
                refresh_token, app.config['JWT_IDENTITY_CLAIM'])
            return make_response(jsonify({
                'access token': access_token,
                'refresh token': refresh_token
            }), 200)
        # replace it to response in future for adding error code
        return make_response(jsonify({'message': 'Invalid Login'}), 401)


class UserLogout(Resource):
    @jwt_required  # Will require accesss token
    def get(self):
        """ User Logout """
        # JWT ID will be blacklisted once user logout
        user_identity = get_jwt_identity()
        all_tokens = get_user_tokens(user_identity)
        ret = [token.to_dict() for token in all_tokens]
        print(ret)
        for r in ret:
            revoke_token(r['token_id'], user_identity)
        #revoke_token(token_id, user_identity)
        return make_response(jsonify({'message': 'Logged out successfully!'}), 200)


class UserTokens(Resource):
    @jwt_required
    def get(self):
        user_identity = get_jwt_identity()
        all_tokens = get_user_tokens(user_identity)
        ret = [token.to_dict() for token in all_tokens]
        return jsonify(ret), 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required  # Requires refresh token to create new access token
    def get(self):
        """ Create a new access token """
        current_user = get_jwt_identity()
        # fresh -> False means that token refresh won't work,
        # user has to sign-in using username and password [login]
        new_token = create_access_token(identity=current_user, fresh=False)
        add_token_to_database(new_token, app.config['JWT_IDENTITY_CLAIM'])
        return make_response(jsonify({'access token': new_token}), 200)


api_login.add_resource(UserList, '/users')
api_login.add_resource(UserActions, '/user')
api_login.add_resource(ChangeEmail, '/user/<email>')
api_login.add_resource(UserLogin, '/login')
api_login.add_resource(UserTokens, '/tokens')
api_login.add_resource(UserLogout, '/logout')
api_login.add_resource(TokenRefresh, '/refresh')
