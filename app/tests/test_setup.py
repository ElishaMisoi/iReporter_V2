import unittest
import json
from app import app

from app.db import create_tables

create_tables.drop_tables()
create_tables.create_tables()


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        self.incident = {
            "id": "1",
            "location": "Nairobi",
            "status": "draft",
            "comment": "another one",
            "Images": "image1, image2",
            "Videos": "video1, video2"
        }

    ''' Generate auth token '''

    def auth_token(self):
        ''' Register a new user '''

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
        user_jwt = json.loads(response.data.decode("utf-8"))['token']
        return user_jwt
