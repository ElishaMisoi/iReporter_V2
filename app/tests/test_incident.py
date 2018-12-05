import unittest
import json
from app import app

class test_incident(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_get_incidents(self):
        # Tests that the end point fetches all records
        response = self.client.get('/api/v1/incidents',
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_single_incident(self):
        # Tests that the end point returns a single record
        incident_details = {
                    "id" : 0,
                    "createdOn" : "Date",  
                    "createdBy" : 1, 
                    "type" : "red-flags",       
                    "location" : "Nairobi",   
                    "status" : "draft",     
                    "comment" : "another one",
                    "Images" : "images",
                    "Videos" : "videos"
            }
        self.client.post('/api/v1/incidents',
                         json=incident_details)
        response = self.client.get('/api/v1/incidents/1',
                                   content_type='application/json')
        msg = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_edit_incident(self):
        # Tests that the end point enables user to edit an incident
        # created incident before status is changed by admin
        incident_details = {
                    "id" : 0,
                    "createdOn" : "Date",  
                    "createdBy" : 1, 
                    "type" : "red-flags",       
                    "location" : "Nairobi",   
                    "status" : "draft",     
                    "comment" : "another one",
                    "Images" : "images",
                    "Videos" : "videos"
            }
        response = self.client.post('/api/v1/incidents',
                                    content_type='application/json',
                                    json=incident_details)
        new_details = {
                    "id" : 0,
                    "createdOn" : "Date",  
                    "createdBy" : 1, 
                    "type" : "red-flags",       
                    "location" : "Nairobi",   
                    "status" : "draft",     
                    "comment" : "another one",
                    "Images" : "images",
                    "Videos" : "videos"
        }
        response = self.client.put('/api/v1/incidents/1',
                                   json=new_details)
        msg = json.loads(response.data)
        self.assertIn("incident updated", msg['message'])
        self.assertEqual(response.status_code, 200)

    def test_delete_incident(self):
        # Tests that the end point enables user edit an incident
        # record when rejected by admin
        incident_details = {
                    "id" : 0,
                    "createdOn" : "Date",  
                    "createdBy" : 1, 
                    "type" : "red-flags",       
                    "location" : "Nairobi",   
                    "status" : "draft",     
                    "comment" : "another one",
                    "Images" : "images",
                    "Videos" : "videos"
            }
        response = self.client.post('/api/v1/incidents',
                                    content_type='application/json',
                                    json=incident_details)
        new_details = {
        }
        response = self.client.delete('/api/v1/incidents/1',
                                      json=new_details)
        msg = json.loads(response.data)
        self.assertIn("deleted incident", msg['message'])
        self.assertEqual(response.status_code, 200)
