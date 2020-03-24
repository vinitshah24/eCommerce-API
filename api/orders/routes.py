""" Routes for orders """

import uuid
from flask import request, jsonify, Blueprint, make_response
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
from api.orders.models import DB, Orders
from api.users.models import DB, Users
from api.products.models import DB, Products
from sqlalchemy.exc import SQLAlchemyError

orders_model = Blueprint('orders', __name__)
api = Api(orders_model)


class OrdersActions(Resource):
    @jwt_required  # Will require accesss token
    def post(self):
        """ Create a new user """
        data = request.get_json()
        public_id = get_jwt_identity()
        order = Orders(
            public_id=str(uuid.uuid4()),
            user_public_id=public_id,
            product_public_id=data['product_id'],
        )
        try:
            DB.session.add(order)
            DB.session.commit()
        except SQLAlchemyError as err:
            error = str(err.__dict__['orig'])
            return make_response(jsonify({'message': error}), 400)
        return make_response(
            jsonify({'message': 'Order placed successfully!'}), 200)

    @jwt_required  # Will require accesss token
    def get(self):
        public_id = get_jwt_identity()
        try:
            order_result = DB.session.query(
                Orders.product_public_id,
                Products.name, Products.company, Products.cost,
                Orders.user_public_id, Users.first_name, Users.last_name
            ).join(
                Products, Orders.product_public_id == Products.public_id
            ).join(
                Users, Orders.user_public_id == Users.public_id
            ).filter(
                Users.public_id == public_id
            ).first()
        except SQLAlchemyError as err:
            error = str(err.__dict__['orig'])
            return make_response(jsonify({'message': error}), 400)
        output = []
        for order in order_result:
            data = {}
            data['product_public_id'] = order_result.product_public_id
            data['name'] = order_result.name
            data['company'] = order_result.company
            data['cost'] = order_result.cost
            data['user_public_id'] = order_result.user_public_id
            data['first_name'] = order_result.first_name
            data['last_name'] = order_result.last_name
        output.append(data)
        return make_response(
            jsonify({'orders': data}), 200)


api.add_resource(OrdersActions, '/order')
