import unittest
import json
from app import app

from app.tests.test_setup import BaseTest
from app.db import create_tables


class Test_Incident(BaseTest):

    def test_add_redflag(self):
        """ Test that API adds a redflag"""
        token = self.auth_token()
        response = self.client.post('api/v2/redflags',
                                    headers=dict(Authorization=token),
                                    content_type='application/json',
                                    data=json.dumps(self.incident))
        
        self.assertEqual(response.status_code, 201)
        
    def test_add_intervention(self):
        """ Test that API adds an intervention"""
        token = self.auth_token()
        response = self.client.post('api/v2/interventions',
                                    headers=dict(Authorization=token),
                                    content_type='application/json',
                                    data=json.dumps(self.incident))
        
        self.assertEqual(response.status_code, 201)
        
    def test_get_single_redflag(self):
        """ Test that API gets single redflag"""
        token = self.auth_token()
        self.client.post('api/v2/redflags',
                            headers=dict(Authorization=token),
                            content_type='application/json',
                            data=json.dumps(self.incident))
        response = self.client.get('api/v2/redflags/16',
                                    headers=dict(Authorization=token),
                                    content_type='application/json')
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_single_intervention(self):
        """ Test that API gets single intervention"""
        token = self.auth_token()
        self.client.post('api/v2/interventions',
                            headers=dict(Authorization=token),
                            content_type='application/json',
                            data=json.dumps(self.incident))
        response = self.client.get('api/v2/interventions/15',
                                    headers=dict(Authorization=token),
                                    content_type='application/json')
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_all_redflags(self):
        """ Test that API adds redflag"""
        token = self.auth_token()
        self.client.post('api/v2/redflags',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(self.incident))
        response = self.client.get('api/v2/redflags',
                                   headers=dict(Authorization=token),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        


    def test_get_all_interventions(self):
        """ Test that API adds redflag"""
        token = self.auth_token()
        self.client.post('api/v2/interventions',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(self.incident))
        response = self.client.get('api/v2/interventions',
                                   headers=dict(Authorization=token),
                                   content_type='application/json')
        print(response.data)
        self.assertEqual(response.status_code, 200)
        


    def test_edit_redflag_location(self):
        """ Test that API can edit a redflag location """
        token = self.auth_token()
        redflag = {
            "id": "1",
            "location": "Nairobi",
            "status": "draft",
            "comment": "another one",
            "Images": "image1, image2",
            "Videos": "video1, video2",
            "type": "red-flag"
        }
        self.client.post('api/v2/redflags',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(redflag))
        self.client.patch('api/v2/redflags/1/location',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(redflag))
        response = self.client.get('api/v2/redflags',
                                   headers=dict(Authorization=token),
                                   content_type='application/json')
        print(response.data)
        self.assertEqual(response.status_code, 200)
        


    def test_edit_intervention_location(self):
        """ Test that API can edit a intervention location """
        token = self.auth_token()
        intervention = {
            "id": "1",
            "location": "Nairobi",
            "status": "draft",
            "comment": "another one",
            "Images": "image1, image2",
            "Videos": "video1, video2",
            "type": "intervention"
        }
        self.client.post('api/v2/interventions',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(intervention))
        self.client.patch('api/v2/interventions/1/location',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(intervention))
        response = self.client.get('api/v2/interventions',
                                   headers=dict(Authorization=token),
                                   content_type='application/json')
        print(response.data)
        self.assertEqual(response.status_code, 200)
        

    
    def test_edit_redflag_comment(self):
        """ Test that API can edit a redflag comment """
        token = self.auth_token()
        redflag = {
            "id": "1",
            "location": "Nairobi",
            "status": "draft",
            "comment": "another one",
            "Images": "image1, image2",
            "Videos": "video1, video2",
            "type": "red-flag"
        }
        self.client.post('api/v2/redflags',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(redflag))
        response = self.client.patch('api/v2/redflags/10/comment',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(redflag))
        print(response.data)
        self.assertEqual(response.status_code, 200)
        


    def test_edit_intervention_comment(self):
        """ Test that API can edit a intervention comment """
        token = self.auth_token()
        intervention = {
            "id": "1",
            "location": "Nairobi",
            "status": "draft",
            "comment": "another one",
            "Images": "image1, image2",
            "Videos": "video1, video2",
            "type": "intervention"
        }
        self.client.post('api/v2/interventions',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(intervention))
        response = self.client.patch('api/v2/interventions/7/comment',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(intervention))
        print(response.data)
        self.assertEqual(response.status_code, 200)
        


    def test_edit_redflag_status(self):
        """ Test that API can edit a redflag status """
        token = self.auth_token()
        redflag = {
            "id": "1",
            "location": "Nairobi",
            "status": "draft",
            "comment": "another one",
            "Images": "image1, image2",
            "Videos": "video1, video2",
            "type": "red-flag"
        }
        self.client.post('api/v2/redflags',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(redflag))
        response = self.client.patch('api/v2/redflags/12/status',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(redflag))
        print(response.data)
        self.assertEqual(response.status_code, 200)
        


    def test_edit_intervention_status(self):
        """ Test that API can edit a intervention status """
        token = self.auth_token()
        intervention = {
            "id": "1",
            "location": "Nairobi",
            "status": "draft",
            "comment": "another one",
            "Images": "image1, image2",
            "Videos": "video1, video2",
            "type": "intervention"
        }
        self.client.post('api/v2/interventions',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(intervention))
        response = self.client.patch('api/v2/interventions/7/status',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(intervention))
        print(response.data)
        self.assertEqual(response.status_code, 200)
        


    def test_delete_redflag(self):
        """ Test that API can delete redflag record """
        token = self.auth_token()
        self.client.post('api/v2/interventions',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(self.incident))
        response = self.client.delete('api/v2/interventions/1',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(self.incident))
        print(response.data)
        self.assertEqual(response.status_code, 200)
        


    def test_delete_intervention(self):
        """ Test that API can delete intervention record """
        token = self.auth_token()
        self.client.post('api/v2/interventions',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(self.incident))
        response = self.client.delete('api/v2/interventions/1',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(self.incident))
        print(response.data)
        self.assertEqual(response.status_code, 200)

    
    def test_only_creators_get_their_redflags(self):
        """ Test only admin can get all redflags """
        # admin = False
        user_details = {
            "firstname": "test_firstn",
            "lastname": "test_lastname",
            "othernames": "test_othernames",
            "email": "not_admin1@email.com",
            "password": "1234555",
            "phoneNumber": "12345678",
            "username": "not admin1",
        }
        response = self.client.post('api/v2/auth/signup',
                         data=json.dumps(user_details),
                         content_type='application/json')

        token = json.loads(response.data.decode("utf-8"))['token']

        self.client.post('api/v2/redflags',
                         headers=dict(Authorization=self.auth_token),
                         content_type='application/json',
                         data=json.dumps(self.incident))
        response1 = self.client.get('api/v2/redflags',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(self.incident))
        print(response1.data)
        self.assertEqual(response.status_code, 201)


    def test_only_creators_get_their_interventions(self):
        """ Test only admin can get all interventions """
        # admin = False
        user_details = {
            "firstname": "test_firstn",
            "lastname": "test_lastname",
            "othernames": "test_othernames",
            "email": "not_admin@email.com",
            "password": "1234555",
            "phoneNumber": "12345678",
            "username": "not admin",
        }
        response = self.client.post('api/v2/auth/signup',
                        data=json.dumps(user_details),
                        content_type='application/json')

        token = json.loads(response.data.decode("utf-8"))['token']

        self.client.post('api/v2/interventions',
                        headers=dict(Authorization=self.auth_token),
                        content_type='application/json',
                        data=json.dumps(self.incident))
        response1 = self.client.get('api/v2/interventions',
                        headers=dict(Authorization=token),
                        content_type='application/json',
                        data=json.dumps(self.incident))
        print(response1.data)
        self.assertEqual(response.status_code, 201)

    def test_redflag_comment_validation(self):
        """ Test redflag comment validation """
        token = self.auth_token()
        redflag = {
            "id": "1",
            "location": "Nairobi",
            "status": "draft",
            "Images": "image1, image2",
            "Videos": "video1, video2",
            "type": "red-flag"
        }
        response = self.client.post('api/v2/interventions',
                        headers=dict(Authorization=token),
                        content_type='application/json',
                        data=json.dumps(redflag))
        print(response.data)
        self.assertEqual(response.status_code, 400)

    def test_intervention_comment_validation(self):
        """ Test intervention comment validation """
        token = self.auth_token()
        redflag = {
            "id": "1",
            "location": "Nairobi",
            "status": "draft",
            "Images": "image1, image2",
            "Videos": "video1, video2",
            "type": "intervention"
        }
        response = self.client.post('api/v2/interventions',
                        headers=dict(Authorization=token),
                        content_type='application/json',
                        data=json.dumps(redflag))
        print(response.data)
        self.assertEqual(response.status_code, 400)

    def test_intervention_location_validation(self):
        """ Test intervention comment validation """
        token = self.auth_token()
        redflag = {
            "id": "1",
            "comment": "test comment",
            "status": "draft",
            "Images": "image1, image2",
            "Videos": "video1, video2",
            "type": "intervention"
        }
        response = self.client.post('api/v2/interventions',
                        headers=dict(Authorization=token),
                        content_type='application/json',
                        data=json.dumps(redflag))
        print(response.data)
        self.assertEqual(response.status_code, 400)

    def test_redflag_location_validation(self):
        """ Test redflag location validation """
        token = self.auth_token()
        redflag = {
            "id": "1",
            "comment": "another one",
            "Images": "image1, image2",
            "status": "draft",
            "Videos": "video1, video2",
            "type": "red-flag"
        }
        response = self.client.patch('api/v2/redflags/10/status',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(redflag))
        print(response.data)
        self.assertEqual(response.status_code, 400)

    def test_intervention_status_validation(self):
        """ Test intervention status validation """
        token = self.auth_token()
        intervention = {
            "id": "1",
            "location": "Nairobi",
            "comment": "another one",
            "Images": "image1, image2",
            "Videos": "video1, video2",
            "type": "intervention",
            "status": ""
        }
        response = self.client.patch('api/v2/interventions/7/status',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(intervention))
        print(response.data)
        self.assertEqual(response.status_code, 400)





    def test_can_only_edit_redflag_location(self):
        """ Test that API can can only edit redflag location """
        token = self.auth_token()
        intervention = {
            "id": "1",
            "location": "Nairobi",
            "status": "draft",
            "comment": "another one",
            "Images": "image1, image2",
            "Videos": "video1, video2",
            "type": "intervention"
        }
        response = self.client.patch('api/v2/redflags/1/location',
                        headers=dict(Authorization=token),
                        content_type='application/json',
                        data=json.dumps(intervention))
        print(response.data)
        self.assertEqual(response.status_code, 400)
        


    def test_can_only_edit_intervention_location(self):
        """ Test that API can can only edit intervention location """
        token = self.auth_token()
        redflag = {
            "id": "1",
            "location": "Nairobi",
            "status": "draft",
            "comment": "another one",
            "Images": "image1, image2",
            "Videos": "video1, video2",
            "type": "red-flag"
        }
        response = self.client.patch('api/v2/interventions/1/location',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(redflag))
        print(response.data)
        self.assertEqual(response.status_code, 400)
        

    
    def test_can_only_edit_redflag_comment(self):
        """ Test that API can can only edit redflag comment """
        token = self.auth_token()
        intervention = {
            "id": "1",
            "location": "Nairobi",
            "status": "draft",
            "comment": "another one",
            "Images": "image1, image2",
            "Videos": "video1, video2",
            "type": "intervention"
        }
        response = self.client.patch('api/v2/redflags/3/comment',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(intervention))
        print(response.data)
        self.assertEqual(response.status_code, 400)
        


    def  test_can_only_edit_intervention_comment(self):
        """ Test that API can can only intervention redflag comment """
        token = self.auth_token()
        redflag = {
            "id": "1",
            "location": "Nairobi",
            "status": "draft",
            "comment": "another one",
            "Images": "image1, image2",
            "Videos": "video1, video2",
            "type": "red-flag"
        }
        response = self.client.patch('api/v2/interventions/7/comment',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(redflag))
        print(response.data)
        self.assertEqual(response.status_code, 400)
        


    def test_can_only_edit_redflag_status(self):
        """ Test that API can only edit redflag status """
        token = self.auth_token()
        intervention = {
            "id": "1",
            "location": "Nairobi",
            "status": "draft",
            "comment": "another one",
            "Images": "image1, image2",
            "Videos": "video1, video2",
            "type": "intervention"
        }
        self.client.post('api/v2/redflags',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(intervention))
        response = self.client.patch('api/v2/redflags/10/status',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(intervention))
        print(response.data)
        self.assertEqual(response.status_code, 400)
        
    def test_can_only_edit_intervention_status(self):
        """ Test that API can only edit intervention status """
        token = self.auth_token()
        redflag = {
            "id": "1",
            "location": "Nairobi",
            "status": "draft",
            "comment": "another one",
            "Images": "image1, image2",
            "Videos": "video1, video2",
            "type": "intervention"
        }
        self.client.post('api/v2/redflags',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(redflag))
        response = self.client.patch('api/v2/redflags/10/status',
                         headers=dict(Authorization=token),
                         content_type='application/json',
                         data=json.dumps(redflag))
        print(response.data)
        self.assertEqual(response.status_code, 400)