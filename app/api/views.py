from flask import jsonify, request, make_response, Response
from flask_restful import Resource
from datetime import datetime
from .models import *
from .validations import *
from functools import wraps
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, verify_jwt_in_request, get_jwt_claims, get_raw_jwt)

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        jwt_holder()
        if get_jwt_claims()['is_admin'] != True:
            return make_response(jsonify({"message": "Admin rights required!"}), 201)
            pass
        return fn(*args, **kwargs)
    return wrapper

def jwt_holder():
    return verify_jwt_in_request()

def attendant_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['is_admin'] != False:
            return make_response(jsonify({"message": "Attendant rights required!"}), 201)
            pass
        return fn(*args, **kwargs)
    return wrapper


def user(email, is_admin, password):
    """ This function returns true if a user is created successfully """
    email=email
    is_admin=is_admin
    password=password
    ValidateRegistration.validate(email, is_admin, password)
    new = User.create_user(email, is_admin, User.generate_hash(password))
    return True

def product_validation(product_name, category, quantity, price):
    """ This function returns validated product details """
    product_name = product_name
    category=category
    quantity=quantity
    price=price
    validated_product=ValidateProduct.validate(product_name, category, quantity, price)
    return validated_product

def product_create(product_name, category, quantity, price):
    """ This function returns a created product """
    ValidateProduct.validate(product_name, category, quantity, price)
    return Product.create_product(product_name, category, quantity, price)

def product_update(product_name, category, quantity, price, product_id):
    """ This function returns an updated product """
    product_validation(product_name, category, quantity, price)
    return Product.update_product(product_name, category, quantity, price, product_id)


def validate_sale(product_id, quantity):
    """ validate sale """
    return ValidateSale.validate(product_id, quantity)

def product_sale(product_id, quantity):
    """ custom product sale """
    validate_sale(product_id, quantity)
    if Sale.create_sale(product_id, quantity)[1]:
        return Sale.create_sale(product_id, quantity)[0]

def error_handling(error):
    """ This function returns well formatted key error messages """
    error = error
    return make_response(jsonify({"message":"{} key missing".format(str(error))}), 400)

class Register(Resource):
    """ User registration """

    def post(self):
        data = request.get_json()
        try:
            user(data['email'], data['is_admin'], data['password'])
            return make_response(jsonify({"message": "User {} was created".format(data['email']), }), 201)
        except KeyError as error:
            return error_handling(error)

    def get(self):
        users=User.get_users()
        return make_response(jsonify({ "message": "success", "users": users }), 200)

class GetSpecificUser(Resource):
    def get(self, user_id):
        user=User.get_specific_user(user_id)
        return make_response(jsonify({ "message": "success", "user": user }), 200)

class Login(Resource):
    """ User login """

    def post(self):
        try:    
            data = request.get_json()
            user = User.login(data['email'], data['password'])
            if user:
                access_token = create_access_token(identity=user[2])
                return make_response(jsonify({
                    "message": "Welcome {}".format(data['email']),
                    "access_token": access_token
                }))
            return make_response(jsonify({"message": "wrong credentials"}), 200)
        except KeyError as error:
            return make_response(jsonify({"message":"{} key missing".format(str(error))}), 400)

class Logout(Resource):
    """ User logout view """
    @jwt_required
    def post(self):
        Blacklist.revoke_token(get_raw_jwt()["jti"], get_raw_jwt()["type"], get_raw_jwt()["identity"], datetime.fromtimestamp(get_raw_jwt()["iat"]).strftime('%Y-%m-%d %H:%M:%S'), datetime.fromtimestamp(get_raw_jwt()["exp"]).strftime('%Y-%m-%d %H:%M:%S'))
        return make_response(jsonify({'message': 'Successfully logged out'}), 200)

class Products(Resource):
    """ Product view """
    @admin_required
    def post(self):
        """ Only admin can add a product """
        try:
            data = request.get_json()
            product_name=data['product_name']
            category=data['category']
            quantity=data['quantity']
            unit_price=data['unit_price']
            return make_response(jsonify({'message': 'Success','product': product_create(product_name, category, quantity, unit_price)}), 201)
        except KeyError as error:
            return error_handling(error)

    @jwt_required
    def get(self):
        """ admin and an attendant should be able to retrieve all products """
        if len(Product.get_products()) > 0:
            return make_response(jsonify({'message': 'Success','products': Product.get_products()}), 200)
        return make_response(jsonify({'message': 'No product record(s) available'}), 404)

class GetSpecificProduct(Resource):
    # """ Get a specific product """

    @jwt_required
    def get(self, product_id):
        if Product.get_specific_product(product_id):
            return make_response(jsonify({ "message": "success", "product": Product.get_specific_product(product_id) }), 200)
        return make_response(jsonify({ "message": "Sorry, such a product does not exist"}), 404)

class UpdateProduct(Resource):
    """ Update a specific product """

    @jwt_required
    def put(self, product_id):
        data = request.get_json()
        try:
            if Product.get_specific_product(product_id):
                if product_id==data['product_id']:  
                    product_update(data['product_name'], data['category'], data['quantity'], data['unit_price'], data['product_id'])
                    return make_response(jsonify({'message': 'Update successful', 'product': Product.get_specific_product(product_id)}), 201)
                return make_response(jsonify({'message': 'Update failed, check product_id'}), 400)
            return make_response(jsonify({'message': 'Sorry, such a product does not exist'}), 400)
        except KeyError as error:
            return error_handling(error)

class DeleteProduct(Resource):
    """ Delete a specific product """

    @admin_required
    def delete(self, product_id):
        """delete product"""
        if Product.get_specific_product(product_id) is not None:
            Product.delete(product_id)
            return make_response(jsonify({'message': 'delete operation successful!'}), 200)
        return make_response(jsonify({'message': 'Sorry, such a product does not exist!'}), 404)

class Sales(Resource):
    """Sales class"""

    @attendant_required
    def post(self):
        try:
            data=request.get_json()
            ValidateSale.validate(data['product_id'], data['quantity'])
            # validate_sale(data['product_id'], data['quantity'])
            if Product.get_specific_product(data['product_id']):
                if Sale.create_sale(data['product_id'], data['quantity']):
                # if product_sale(data['product_id'], data['quantity']):
                    return make_response(jsonify(Sale.create_sale(data['product_id'], data['quantity'])), 201)
                return make_response(jsonify({'message': 'Insufficient stock'}), 200)
            return make_response(jsonify({'message': 'Warning! You are attempting to sale a non-existent product'}), 200)
        except KeyError as error:
            return error_handling(error)

    @admin_required
    def get(self):
        """ admin should be able to retrieve all sales """
        if len(Sale.get_sales()) > 0:
            return make_response(jsonify({'message': 'Success','sales': Sale.get_sales()}), 200)
        return make_response(jsonify({'message': 'No sale record(s) available'}), 200)

class GetSpecificSale(Resource):
    # """ Get a specific sale item """

    @attendant_required
    def get(self, sale_id):
        if Sale.get_specific_sale(sale_id):
            return make_response(jsonify({ "message": "Success", "sale": Sale.get_specific_sale(sale_id) }), 200)
        return make_response(jsonify({ "message": "Sorry, such a sale does not exist"}), 200)