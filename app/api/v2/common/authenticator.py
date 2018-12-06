from functools import wraps
from flask import jsonify, request
import jwt
from app.db.config import open_connection, close_connection


def authenticate(func):
    ''' Decorator for endpoint functions '''
    @wraps(func)
    def authorize(*args, **kwargs):
        ''' Check for the user's authentication token in header '''

        if 'Authorization' not in request.headers:
            response = jsonify({
                "message": "Missing Authorization header"
            })
            response.status_code = 401
            return response
        
        jwt_token = request.headers['Authorization']
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("select token from blacklist where token = '{}'".format(jwt_token))
        blacklisted = cur.fetchone()

        if blacklisted:
            response = jsonify({
                "message": "Account logged out. Please log in to continue"
            })
            response.status_code = 401
            cur.close()
            close_connection(conn)
            return response

        try:
            identity = jwt.decode(jwt_token, 'secret')['sub']
            return func(identity, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            response = jsonify({
                "message": "Your token has expired. Please log in to continue"
            })
            response.status_code = 401
            return response

        except jwt.InvalidTokenError:
            response = jsonify({
                "message": "Invalid token. Please log in or sign up to continue"
            })
            response.status_code = 401
            return response

    return authorize