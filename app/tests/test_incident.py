import unittest
import json
from app import app

from app.tests.test_setup import BaseTest
from app.db import create_tables

class Test_Incident(BaseTest):
    # def setUp(self):
    #     self.client = app.test_client()

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




    
    # def test_get_single_redflag(self):
    #     """ Test that API adds redflag"""
    #     token = self.auth_token()
    #     self.client.post('api/v2/redflags', 
    #                                 headers=dict(Authorization=token),
    #                                 content_type='application/json', 
    #                                 data=json.dumps(self.incident))
    #     response = self.client.get('api/v2/redflags/1', 
    #                                 headers=dict(Authorization=token),
    #                                 content_type='application/json')
    #     print(response.data)
    #     self.assertEqual(response.status_code, 200)


    # def test_get_single_intervention(self):
    #     """ Test that API adds intervention"""
    #     token = self.auth_token()
    #     self.client.post('api/v2/interventions', 
    #                                 headers=dict(Authorization=token),
    #                                 content_type='application/json', 
    #                                 data=json.dumps(self.incident))
    #     response = self.client.get('api/v2/interventions/1', 
    #                                 headers=dict(Authorization=token),
    #                                 content_type='application/json')
    #     self.assertEqual(response.status_code, 200)


    # def test_edit_redflag_status(self):
    #     """ Test that API adds redflag"""
    #     token = self.auth_token()
    #     self.client.post('api/v2/interventions', 
    #                                 headers=dict(Authorization=token),
    #                                 content_type='application/json', 
    #                                 data=json.dumps(self.incident))
    #     response =  self.client.patch('api/v2/interventions/1/status', 
    #                                 headers=dict(Authorization=token),
    #                                 content_type='application/json', 
    #                                 data=json.dumps(self.incident.update(status = 'new status')))
        
    #     print(response.data)
    #     self.assertEqual(response.status_code, 200)

    # def test_edit_redflag_comment(self):
    #     """ Test that API adds redflag"""

    # def test_edit_redflag_location(self):
    #     """ Test that API adds redflag"""

    # def test_edit_intervention_status(self):
    #     """ Test that API adds redflag"""

    # def test_edit_intervention_comment(self):
    #     """ Test that API adds redflag"""

    # def test_edit_intervention_location(self):
    #     """ Test that API adds redflag"""

    # def test_delete_redflag(self):
    #     """ Test that API adds redflag"""

    # def test_delete_intervention(self):
    #     """ Test that API adds redflag"""
