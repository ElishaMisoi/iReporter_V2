import jwt
from flask import jsonify
from datetime import datetime, timedelta
from passlib.apps import custom_app_context as pwd_hash

from app.db.config import open_connection

conn = open_connection()
cur =conn.cursor()

class User:
    # user class
    def __init__(self,email, password):
        self.email = email
        self.password = password
    
    def signup(self, username, firstname, lastname, othernames,  phoneNumber):
        #registering a new user
        user_exists = self.user_exists()

        if user_exists:
            response = jsonify({
                "message": "An account with that email already exists"
            })
            response.status_code = 409
            return response

        else:
            hashed_pw = pwd_hash.encrypt(self.password)
            conn = open_connection()
            cur = conn.cursor()

            cur.execute("INSERT INTO users(firstname, lastname, othernames, email, phoneNumber, username, password) values('{}','{}','{}','{}','{}','{}','{}')".format(firstname,lastname,othernames,self.email,phoneNumber,username,hashed_pw))

            cur.execute("select id from users where email = '{}' ".format(self.email))
            user_id = cur.fetchone()[0]
            token = self.generate_token(user_id)
            cur.close()
            conn.commit()

            user_info = self.get_user_details()
            response = jsonify({
                "message": "User registered successfully",
                "token": token.decode("utf-8"),
                "user": user_info
            })
            response.status_code = 200
            return response

    
    def user_exists(self):
        #checking if user already exists
        cur.execute("select * from users where email='{}'".format(self.email))
        user = cur.fetchone()
        return user

    
    def get_user_details(self):
        # getting one user
        user = self.user_exists()

        if user:
            user_data = {}
            user_data['id'] = user[0]
            user_data['firstname'] = user[1]
            user_data['lastname'] = user[2]
            user_data['othernames'] = user[3]
            user_data['email'] = user[4]
            user_data['phoneNumber'] = user[5]
            user_data['username'] = user[6]
            user_data['registered'] = user[8]
            user_data['isAdmin'] = user[9]
            
            return user_data

        else:
            response = jsonify({
                "message": "User not found"
            })
            response.status_code = 404
            return response

    def generate_token(self, user_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                'secret',
                algorithm='HS256'
            )
        except Exception as e:
            return e


    def login(self):
        #logging in an existing user
        user_exists = self.user_exists()

        if user_exists:

            pw_match = self.verify_password(user_exists[7])

            if pw_match:
                token = self.generate_token(user_exists[0])

                user_info = self.get_user_details()

                response = jsonify({
                    "message": "Login successful",
                    "token": token.decode("utf-8"),
                    "user": user_info
                })
                response.status_code = 200
                return response

            else:
                response = jsonify({
                    "message": "Incorrect password"
                })
                response.status_code = 401
                return response

        else:
            response = jsonify({
                "message": "The email used is not registered. Try creating a new account"
            })
            response.status_code = 401
        return response


    def verify_password(self, stored_pwd):
        #confirm password 
        return pwd_hash.verify(self.password, stored_pwd)

