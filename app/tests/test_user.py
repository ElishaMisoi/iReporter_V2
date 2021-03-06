import unittest
import json
from app import app

from app.db import create_tables


create_tables.drop_tables()
create_tables.create_tables()


class UserTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    ''' User tests '''

    def test_signup(self):
        ''' Register a new user '''

        user_details = {
            "firstname": "test_firstn",
            "lastname": "test_lastname",
            "othernames": "test_othernames",
            "email": "signup_email@email.com",
            "password": "1234",
            "phoneNumber": "12345678",
            "username": "test_signup_user"
        }
        response = self.client.post('api/v2/auth/signup',
                                    json=user_details)
        json.loads(response.data)
        self.assertEqual(response.status_code, 201)

    def test_email_already_exist(self):
        ''' Test that email already exists '''

        user_details = {
            "firstname": "test_firstn",
            "lastname": "test_lastname",
            "othernames": "test_othernames",
            "email": "email@email.com",
            "password": "1234",
            "phoneNumber": "12345678",
            "username": "test_user"
        }
        user_details1 = {
            "firstname": "test_firstn",
            "lastname": "test_lastname",
            "othernames": "test_othernames",
            "email": "email@email.com",
            "password": "1234",
            "phoneNumber": "12345678",
            "username": "test_user1"
        }
        self.client.post('api/v2/auth/signup',
                         json=user_details)
        response = self.client.post('api/v2/auth/signup',
                                    json=user_details1)
        json.loads(response.data)
        self.assertEqual(response.status_code, 409)

    def test_email_exists(self):
        ''' Should not register user with an already existing email '''

        user_details = {
            "firstname": "test_firstn",
            "lastname": "test_lastname",
            "othernames": "test_othernames",
            "email": "email1@email.com",
            "password": "1234",
            "phoneNumber": "12345678",
            "username": "test_user1"
        }
        self.client.post('api/v2/auth/signup',
                         json=user_details)
        response = self.client.post('api/v2/auth/signup',
                                    json=user_details)
        self.assertEqual(response.status_code, 409)

    def test_special_characters(self):

        user_details = {
            "firstname": "test_firstn",
            "lastname": "test_lastname",
            "othernames": "test_othernames",
            "email": "!!!!!!!",
            "password": "1234",
            "phoneNumber": "12345678",
            "username": "test_user1"
        }
        result = self.client.post('/api/v2/auth/signup',
                                  data=json.dumps(user_details),
                                  content_type='application/json')
        self.assertEqual(result.status_code, 400)

    def test_empty_email_signup(self):
        ''' Should not register user with a missing email '''

        user_details = {
            "firstname": "test_firstn",
            "lastname": "test_lastname",
            "othernames": "test_othernames",
            "email": "",
            "password": "1234",
            "phoneNumber": "12345678",
            "username": "test_user1"
        }
        result = self.client.post('/api/v2/auth/signup',
                                  data=json.dumps(user_details),
                                  content_type='application/json')
        self.assertEqual(result.status_code, 400)

    def test_empty_pass_signup(self):
        ''' Should not register user with a missing password '''

        user_details = {
            "firstname": "test_firstn",
            "lastname": "test_lastname",
            "othernames": "test_othernames",
            "email": "test@email.com",
            "password": "",
            "phoneNumber": "12345678",
            "username": "test_user1"
        }
        result = self.client.post('/api/v2/auth/signup',
                                  data=json.dumps(user_details),
                                  content_type='application/json')
        self.assertEqual(result.status_code, 400)

    def test_user_login(self):
        ''' Should log in an existing user '''

        user_details = {
            "firstname": "test_firstn",
            "lastname": "test_lastname",
            "othernames": "test_othernames",
            "email": "email@email.com",
            "password": "1234",
            "phoneNumber": "12345678",
            "username": "test_user"
        }
        self.client.post('api/v2/auth/signup',
                         json=user_details)
        result = self.client.post('/api/v2/auth/login',
                                  data=json.dumps(user_details),
                                  content_type='application/json')
        print(result)
        self.assertEqual(result.status_code, 200)

    def test_email_format_signup(self):
        ''' Should not register user with invalid email '''

        user_details = {
            "firstname": "test_firstn",
            "lastname": "test_lastname",
            "othernames": "test_othernames",
            "email": "email",
            "password": "1234",
            "phoneNumber": "12345678",
            "username": "test_user"
        }
        result = self.client.post('/api/v2/auth/signup',
                                  data=json.dumps(user_details),
                                  content_type='application/json')
        self.assertEqual(result.status_code, 400)

    def test_incorrect_email_login(self):
        ''' Should not login user using wrong email '''

        result = self.client.post('/api/v2/auth/login',
                                  data=json.dumps(dict(
                                      email='wrong@domain.com',
                                      password='Very_secret'
                                  )),
                                  content_type='application/json')
        self.assertEqual(result.status_code, 401)

    def test_incorrect_password_login(self):
        ''' Should not login user using wrong password '''

        result = self.client.post('/api/v2/auth/login',
                                  data=json.dumps(dict(
                                      email='sample@domain.com',
                                      password='som-wrong'
                                  )),
                                  content_type='application/json')

        self.assertEqual(result.status_code, 401)

    def test_empty_email_login(self):
        ''' Should not login user with a missing parameter '''

        result = self.client.post('/api/v2/auth/login',
                                  data=json.dumps({
                                      "email": '',
                                      "password": "password"
                                  }),
                                  content_type='application/json')

        self.assertEqual(result.status_code, 400)

    def test_email_format_login(self):
        ''' Should not login user with invalid email '''

        user_info = {
            "email": 'domain.com',
            "password": 'Very_secret'
        }
        result = self.client.post('/api/v2/auth/login',
                                  data=json.dumps(user_info),
                                  content_type='application/json')
        self.assertEqual(result.status_code, 400)

    def test_get_all_users(self):
        ''' Test get all users '''

        user_details = {
            "firstname": "test_firstn",
            "lastname": "test_lastname",
            "othernames": "test_othernames",
            "email": "email@email.com",
            "password": "1234",
            "phoneNumber": "12345678",
            "username": "test_user"
        }
        self.client.post('api/v2/auth/signup',
                         data=json.dumps(user_details),
                         content_type='application/json')
        response = self.client.post('api/v2/auth/login',
                                    data=json.dumps(user_details),
                                    content_type='application/json')
        token = json.loads(response.data.decode("utf-8"))['token']

        result = self.client.get('/api/v2/users',
                                 headers=dict(Authorization=token),
                                 content_type='application/json')
        self.assertEqual(result.status_code, 200)

    def test_get_single_user(self):
        ''' Test get single user '''

        user_details = {
            "firstname": "test_firstn",
            "lastname": "test_lastname",
            "othernames": "test_othernames",
            "email": "email@email.com",
            "password": "1234",
            "phoneNumber": "12345678",
            "username": "test_user"
        }
        self.client.post('api/v2/auth/signup',
                         data=json.dumps(user_details),
                         content_type='application/json')
        response = self.client.post('api/v2/auth/login',
                                    data=json.dumps(user_details),
                                    content_type='application/json')
        token = json.loads(response.data.decode("utf-8"))['token']

        result = self.client.get('/api/v2/users/1',
                                 headers=dict(Authorization=token),
                                 content_type='application/json')
        self.assertEqual(result.status_code, 200)

    def test_delete_user(self):
        ''' Test delete user '''

        user_details = {
            "firstname": "test_firstn",
            "lastname": "test_lastname",
            "othernames": "test_othernames",
            "email": "authemail@email.com",
            "password": "1234555",
            "phoneNumber": "12345678",
            "username": "test_user69",
            "isAdmin": "True"
        }
        self.client.post('api/v2/auth/signup',
                         data=json.dumps(user_details),
                         content_type='application/json')
        response = self.client.post('api/v2/auth/login',
                                    data=json.dumps(user_details),
                                    content_type='application/json')
        token = json.loads(response.data.decode("utf-8"))['token']

        result = self.client.delete('/api/v2/users/2',
                                    headers=dict(Authorization=token),
                                    content_type='application/json')
        self.assertEqual(result.status_code, 200)

    def test_user_does_not_exist(self):
        ''' Test delete user '''

        user_details = {
            "firstname": "test_firstn",
            "lastname": "test_lastname",
            "othernames": "test_othernames",
            "email": "authemail1@email.com",
            "password": "1234555",
            "phoneNumber": "12345678",
            "username": "test_user691",
            "isAdmin": "True"
        }
        self.client.post('api/v2/auth/signup',
                         data=json.dumps(user_details),
                         content_type='application/json')
        response = self.client.post('api/v2/auth/login',
                                    data=json.dumps(user_details),
                                    content_type='application/json')
        token = json.loads(response.data.decode("utf-8"))['token']

        result = self.client.delete('/api/v2/users/200',
                                    headers=dict(Authorization=token),
                                    content_type='application/json')
        self.assertEqual(result.status_code, 200)
