import unittest
import json
from app import app

from app.tests.auth import BaseTest
from app.db import create_tables

class Test_Incident(BaseTest):
    # def setUp(self):
    #     self.client = app.test_client()

    def test_add_redflag(self):
        """ Test that API adds a redflag"""
        token = self.auth_token()
        incident = {
                "location" : "Nairobi",   
                "status" : "draft",     
                "comment" : "another one",
                "Images" : "image1, image2",
                "Videos" : "video1, video2"
                }
        response = self.client.post('api/v2/redflags', 
                                    headers=dict(Authorization=token),
                                    content_type='application/json', 
                                    data=json.dumps(incident))

        self.assertEqual(response.status_code, 201)

    
    def test_add_intervention(self):
        """ Test that API adds an intervention"""
        token = self.auth_token()
        incident = {
                "location" : "Nairobi",   
                "status" : "draft",     
                "comment" : "another one",
                "Images" : "image1, image2",
                "Videos" : "video1, video2"
                }
        response = self.client.post('api/v2/interventions', 
                                    headers=dict(Authorization=token),
                                    content_type='application/json', 
                                    data=json.dumps(incident))

        self.assertEqual(response.status_code, 201)

    # def test_get_all_redflags(self):
    #     """ Test that API adds redflag"""

    # def test_get_all_interventions(self):
    #     """ Test that API adds redflag"""

    # def test_get_single_redflag(self):
    #     """ Test that API adds redflag"""
    
    # def test_get_single_intervention(self):
    #     """ Test that API adds redflag"""

    # def test_edit_redflag_status(self):
    #     """ Test that API adds redflag"""

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


    # def test_get_incidents(self):
    #     # Tests that the end point fetches all records
    #     response = self.client.get('/api/v1/incidents',
    #                                content_type='application/json')
    #     self.assertEqual(response.status_code, 200)

    # def test_get_single_incident(self):
    #     # Tests that the end point returns a single record
    #     incident_details = {
    #                 "id" : 0,
    #                 "createdOn" : "Date",  
    #                 "createdBy" : 1, 
    #                 "type" : "red-flags",       
    #                 "location" : "Nairobi",   
    #                 "status" : "draft",     
    #                 "comment" : "another one",
    #                 "Images" : "images",
    #                 "Videos" : "videos"
    #         }
    #     self.client.post('/api/v1/incidents',
    #                      json=incident_details)
    #     response = self.client.get('/api/v1/incidents/1',
    #                                content_type='application/json')
    #     self.assertEqual(response.status_code, 200)

    # def test_edit_incident(self):
    #     # Tests that the end point enables user to edit an incident
    #     # created incident before status is changed by admin
    #     incident_details = {
    #                 "id" : 0,
    #                 "createdOn" : "Date",  
    #                 "createdBy" : 1, 
    #                 "type" : "red-flags",       
    #                 "location" : "Nairobi",   
    #                 "status" : "draft",     
    #                 "comment" : "another one",
    #                 "Images" : "images",
    #                 "Videos" : "videos"
    #         }
    #     response = self.client.post('/api/v1/incidents',
    #                                 content_type='application/json',
    #                                 json=incident_details)
    #     new_details = {
    #                 "id" : 0,
    #                 "createdOn" : "Date",  
    #                 "createdBy" : 1, 
    #                 "type" : "red-flags",       
    #                 "location" : "Nairobi",   
    #                 "status" : "draft",     
    #                 "comment" : "another one",
    #                 "Images" : "images",
    #                 "Videos" : "videos"
    #     }
    #     response = self.client.put('/api/v1/incidents/1',
    #                                json=new_details)
    #     msg = json.loads(response.data)
    #     self.assertIn("incident updated", msg['message'])
    #     self.assertEqual(response.status_code, 200)

    # def test_delete_incident(self):
    #     # Tests that the end point enables user edit an incident
    #     # record when rejected by admin
    #     incident_details = {
    #                 "id" : 0,
    #                 "createdOn" : "Date",  
    #                 "createdBy" : 1, 
    #                 "type" : "red-flags",       
    #                 "location" : "Nairobi",   
    #                 "status" : "draft",     
    #                 "comment" : "another one",
    #                 "Images" : "images",
    #                 "Videos" : "videos"
    #         }
    #     response = self.client.post('/api/v1/incidents',
    #                                 content_type='application/json',
    #                                 json=incident_details)
    #     new_details = {
    #     }
    #     response = self.client.delete('/api/v1/incidents/1',
    #                                   json=new_details)
    #     msg = json.loads(response.data)
    #     self.assertIn("deleted incident", msg['message'])
    #     self.assertEqual(response.status_code, 200)
