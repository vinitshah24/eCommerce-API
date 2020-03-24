""" Routes for products """

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
from api.products.models import DB, Products
from sqlalchemy.exc import SQLAlchemyError

products_model = Blueprint('products', __name__)
api = Api(products_model)


class ProductActions(Resource):
    def post(self):
        """ Create a new user """
        data = request.get_json()
        product = Products(
            public_id=str(uuid.uuid4()),
            name=data['name'],
            company=data['company'],
            description=data['description'],
            category=data['category'],
            cost=data['cost'],
        )
        try:
            DB.session.add(product)
            DB.session.commit()
        except SQLAlchemyError as err:
            error = str(err.__dict__['orig'])
            return make_response(jsonify({'message': error}), 400)
        return make_response(
            jsonify({'message': 'User created successfully!'}), 200)

    def get(self):
        products = Products.query.all()
        output = []
        for product in products:
            data = {}
            data['public_id'] = product.public_id
            data['name'] = product.name
            data['company'] = product.company
            data['description'] = product.description
            data['category'] = product.category
            data['cost'] = product.cost
        output.append(data)
        return make_response(jsonify({'products': output}), 200)


class ProductDetails(Resource):
    def get(self, public_id):
        """ Get Product Details """
        product = Products.query.filter_by(public_id=public_id).first()
        data = {}
        data['public_id'] = product.public_id
        data['name'] = product.name
        data['company'] = product.company
        data['description'] = product.description
        data['category'] = product.category
        data['cost'] = product.cost
        return make_response(jsonify({'product': data}), 200)


api.add_resource(ProductActions, '/product')
api.add_resource(ProductDetails, '/product/<public_id>')
