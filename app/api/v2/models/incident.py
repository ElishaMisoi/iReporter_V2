from flask import jsonify

from app.db.config import open_connection, close_connection

conn = open_connection()
cur = conn.cursor()


class Incident:
    # incident class
    def __init__(self, createdBy, type, location,
                 status, Images, Videos, comment):
        self.createdBy = createdBy
        self.type = type
        self.location = location
        self.status = status
        self.Images = Images
        self.Videos = Videos
        self.comment = comment

    def create_incident(self):
        # creating an incident
        conn = open_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO incidents(createdBy, type, location, status, Images, Videos, comment) values('{}','{}','{}','{}','{}','{}','{}')".format(
                self.createdBy,
                self.type,
                self.location,
                self.status,
                self.Images,
                self.Videos,
                self.comment))
        conn.commit()
        cur.execute("select * from incidents")
        incident = cur.fetchall()[-1]

        cur.close()

        print(incident)
        incident_type = ''

        if self.type == 'red-flag':
            incident_type = 'red-flag'
        else:
            incident_type = 'intervention'

        response = jsonify({
            "status": 201,
            "data": incident,
            "message": "Created " + incident_type + " record"
        }), 201

        return response
