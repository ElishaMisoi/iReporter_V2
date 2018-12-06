from flask import Flask, jsonify, request
from app.api.v2.models.incident import Incident
from datetime import datetime
from app.api.v2.common.validator import email, required
from marshmallow import ValidationError, Schema, fields
from app.api.v2.views import api

incidents_list = []

redflags_list = []

class IncidentSchema(Schema):
    #Represents the schema for incidents
    type = fields.Str(required=True, validate=(required))
    comment = fields.Str(required=True, validate=(required))
    location = fields.Str(required=True, validate=(required))
    id = fields.Int(required=False)
    createdOn = fields.Str(required=False)
    createdBy = fields.Int(required=False)
    Images = fields.Str(required=False)
    status = fields.Str(required=False)
    Videos = fields.Str(required=False)

class RedflagSchema(Schema):
    #Represents the schema for redflags
    type = fields.Str(required=False)
    comment = fields.Str(required=True, validate=(required))
    location = fields.Str(required=True, validate=(required))
    id = fields.Int(required=False)
    createdOn = fields.Str(required=False)
    createdBy = fields.Int(required=False)
    Images = fields.Str(required=False)
    status = fields.Str(required=False)
    Videos = fields.Str(required=False)

@api.route('/incidents', methods=['POST'])
def create_incident():
    # posting an incident
    data, errors = IncidentSchema().load(request.get_json())
    
    if errors:
            return jsonify({
              "errors": errors, 
              "status": 400}), 400

    id = len(incidents_list)+1
    createdOn = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    createdBy = id = len(incidents_list)+1
    incident = Incident(id, createdOn, createdBy, data['type'], data['location'],
                data['status'],
                data['Images'], data['Videos'], data['comment'])

    incidents_list.append(incident)

    return jsonify({
        "message": "Incident created",
        "status": 201,
        }), 201


@api.route('/incidents', methods=['GET'])
def get_incidents():
    # getting all incidents
    Incidents = [incident.get_incident() for incident in incidents_list]
    return jsonify({"data": Incidents})


@api.route('/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    my_incident = []
    incident = incidents_list[incident_id - 1]
    my_incident.append(incident.get_incident())
    return jsonify({
        "data": my_incident
        }), 200


@api.route('/incidents/<int:incident_id>', methods=['PUT'])
def edit_incident(incident_id):
    # function for editing an incident
    if incident_id == 0 or incident_id > len(incidents_list):
        return jsonify({"message": "Index is out of range"}), 400
    data = request.get_json()
    for incident in incidents_list:
        if int(incident.id) == int(incident_id):
            incident.type = data['type']
            incident.id = data['id']
            incident.comment = data['comment']
            incident.location = data['location']
            incident.status = 200
            incident.images = data['Images']
            incident.videos = data['Videos']
            incident.createdBy = data['createdBy']
            incident.createdOn = data['createdOn']
    return jsonify({
        "status": 200,
        "message": "incident updated"
        }), 200


@api.route('/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    # deleting an incident
    if incident_id == 0 or incident_id > len(incidents_list):
        return jsonify({"message": "Index out of range"}), 400
    for incident in incidents_list:
        if incident.id == incident_id:
            incidents_list.remove(incident)
    return jsonify({
        "status": 200,
        "message": "deleted incident"
        }), 200


@api.route('/red-flags', methods=['GET'])
def get_redflags():
    # getting all red-flags
    Redflags = [incident.get_incident() for incident in redflags_list]
    if len(redflags_list) > 0:
     return jsonify({
         "data": Redflags,
         "status" : 200
        }, 200)
    else:
     return jsonify({
             "error": "no red-flags found",
             "status": 404
             }, 404)


@api.route('/red-flags', methods=['POST'])
def create_redflag():
    # function for creating a red-flag
    data, errors = RedflagSchema().load(request.get_json())
    
    if errors:
            return jsonify({
              "errors": errors, 
              "status": 422}), 422

    id = len(redflags_list)+1
    createdOn = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    createdBy = id = len(redflags_list)+1
    type = "red-flag"
    red_flag = Incident(id, createdOn, createdBy, type, data['location'],
                data['status'],
                data['Images'], data['Videos'], data['comment'])

    redflags_list.append(red_flag)

    return jsonify({
        "message": "Red-flag created",
        "status": 201,
        }), 201


@api.route('/red-flags/<int:redflag_id>', methods=['GET'])
def get_single_redflag(redflag_id):
    # function for getting a single redflag
    my_incident = []
    incident = redflags_list[redflag_id - 1]
    my_incident.append(incident.get_incident())
    return jsonify({
        "data": my_incident
        }), 200


@api.route('/red-flags/<int:redflag_id>/location', methods=['PATCH'])
def edit_iredflag_location(redflag_id):
    # function for editing redflag location
    if redflag_id == 0 or redflag_id > len(redflags_list):
        return jsonify({"message": "Index is out of range"}), 400
    data = request.get_json()
    for incident in redflags_list:
        if int(incident.id) == int(redflag_id):
            incident.comment = data['location']
            return jsonify({
                "status": 200,
                "message": "red-flag updated"
                }), 200
        else:
         return jsonify({
             "error": "the red-flag was not found",
             "status": 404
             }, 404)


@api.route('/red-flags/<int:redflag_id>/comment', methods=['PATCH'])
def edit_redflag_comment(redflag_id):
    # function for editing redflag comment
    if redflag_id == 0 or redflag_id > len(redflags_list):
        return jsonify({"message": "Index is out of range"}), 400
    data = request.get_json()
    for incident in redflags_list:
        if int(incident.id) == int(redflag_id):
            incident.comment = data['comment']
            return jsonify({
                "status": 200,
                "message": "incident updated"
                }), 200
        else:
         return jsonify({
             "error": "the red-flag was not found",
             "status": 404
             }, 404)


@api.route('/red-flags/<int:redflag_id>', methods=['DELETE'])
def delete_redflag(redflag_id):
    # deleting a redflag
    if redflag_id == 0 or redflag_id > len(redflags_list):
        return jsonify({"message": "Index out of range"}), 400
    for incident in redflags_list:
        if incident.id == redflag_id:
            redflags_list.remove(incident)
    return jsonify({
        "status": 200,
        "message": "deleted red-flag"
        }), 200

