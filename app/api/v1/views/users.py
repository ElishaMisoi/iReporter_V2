from flask import Flask, jsonify, request
from app.api.v1.models.users import User
from datetime import datetime
from app.api.v1.common.validator import email, required
from marshmallow import ValidationError, Schema, fields
from app.api.v1.views import api

users = []

class UserSchema(Schema):
    #Represents the schema for users
    firstname = fields.Str(required=True, validate=(required))
    lastname = fields.Str(required=True, validate=(required))
    username = fields.Str(required=True, validate=(required))
    email = fields.Email(required=True, validate=(email))
    othernames = fields.Str(required=True, validate=(required))
    password = fields.Str(required=True, validate=(required))
    password_confirm = fields.Str(required=True, validate=(required))
    phoneNumber = fields.Str(required=True, validate=(required))

@api.route('/users', methods=['POST'])
def create_user():
    # creating a user
    data, errors = UserSchema().load(request.get_json())

    if errors:
            return jsonify({
              "errors": errors, 
              "status": 422}), 422

    id = len(users)+1
    registered = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    isAdmin = False

    user = User(id, data['firstname'], data['lastname'],
                data['othernames'], data['email'], data['phoneNumber'],
                data['username'], registered, isAdmin, data['password'], data['password_confirm'])
    
    users.append(user)

    return jsonify({
        "message": "User created",
        "status": 201
        }), 201


@api.route('/users', methods=['GET'])
def get_users():
    # getting all users
    user = [user.get_user_details() for user in users]
    return jsonify({
        "data": user
        }), 200


@api.route('/users/<int:user_id>', methods=['GET'])
# getting one user
def get_one_user(user_id):
    fetched_user = []
    user = users[user_id - 1]
    fetched_user.append(user.get_user_details())
    return jsonify({
        "data": fetched_user}
        ), 200


@api.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # deleting a user
    if user_id == 0 or user_id > len(users):
        return jsonify({"message": "Index out of range"}), 400
    for user in users:
        if user.id == user_id:
            users.remove(user)
    return jsonify({"message": "account successfully deleted"}), 200