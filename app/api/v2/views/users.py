from flask import Flask, jsonify, request
from marshmallow import ValidationError, Schema, fields

from app.db.config import open_connection, close_connection
from app.api.v2.models.users import User
from app.api.v2.common.authenticator import authenticate
from app.api.v2.common.validator import email, required
from app.api.v2.views import api


class SignUpSchema(Schema):
    # Represents the schema for users
    firstname = fields.Str(required=True, validate=(required))
    lastname = fields.Str(required=True, validate=(required))
    username = fields.Str(required=True, validate=(required))
    email = fields.Email(required=True, validate=(email))
    othernames = fields.Str(required=True, validate=(required))
    password = fields.Str(required=True, validate=(required))
    phoneNumber = fields.Str(required=True, validate=(required))


class SignInSchema(Schema):
    # Represents the schema for users
    email = fields.Email(required=True, validate=(email))
    password = fields.Str(required=True, validate=(required))


def email_exists(email):
    """ Check if a user exists in the db """
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("SELECT * from users WHERE email='{}'".format(email))
    user = cur.fetchone()
    return user


@api.route('/auth/signup', methods=['POST'])
def create_user():
    # creating a user
    conn = open_connection()
    cur = conn.cursor()

    data, errors = SignUpSchema().load(request.get_json())

    if errors:
        return jsonify({
            "errors": errors,
            "status": 400}), 400

    cur.execute(
        "select * from users where username = '{}'".format(data['username']))
    user_names = cur.fetchall()

    if len(user_names) > 0:
        response = jsonify({"message": "The username taken"})
        response.status_code = 409
        return response

    if email_exists(data['email']):
        response = jsonify(
            {"message": "The email is already registered, try login in"})
        response.status_code = 409
        return response

    user = User(data['email'], data['password'])

    register = user.signup(
        data['username'],
        data['firstname'],
        data['lastname'],
        data['othernames'],
        data['phoneNumber'],
    )
    close_connection(conn)

    return register


@api.route('/auth/login', methods=['POST'])
def login_user():
    # login in user
    data, errors = SignInSchema().load(request.get_json())

    if errors:
        return jsonify({
            "errors": errors,
            "status": 400}), 400

    user = User(data['email'], data['password'])

    login = user.login()
    return login


@api.route('/users', methods=['GET'])
@authenticate
def get_users(identity):
    # getting all users
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("select * from users")
    users = cur.fetchall()
    close_connection(conn)
    return jsonify({
        "data": users
    }), 200


@api.route('/users/<int:user_id>', methods=['GET'])
@authenticate
def get_one_user(identity, user_id):
    # getting one user
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("select * from users where id = {}".format(user_id))
    user_data = cur.fetchone()
    close_connection(conn)
    return jsonify({
        "data": user_data
    }), 200


@api.route('/users/<int:user_id>', methods=['DELETE'])
@authenticate
def delete_user(identity, user_id):
    # deleting a user
    conn = open_connection()
    cur = conn.cursor()

    cur.execute("select * from users where id = '{}'".format(user_id))
    users = cur.fetchall()

    if len(users < 0):
        close_connection(conn)
        return jsonify({
            "message": "User does not exist"
        }), 200

    cur.execute("delete * from users where id = {}".format(user_id))
    conn.commit()
    close_connection(conn)
    return jsonify({
        "message": "User successfully deleted"
    }), 200
