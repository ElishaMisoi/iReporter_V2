from flask import Flask, jsonify, request
from marshmallow import ValidationError, Schema, fields

from app.api.v2.models.incident import Incident
from app.api.v2.common.validator import email, required
from app.api.v2.views import api
from app.api.v2.common.authenticator import authenticate
from app.db.config import open_connection, close_connection

conn = open_connection()
cur = conn.cursor()

class IncidentSchema(Schema):
    #Represents the schema for incidents
    type = fields.Str(required=False)
    comment = fields.Str(required=True, validate=(required))
    location = fields.Str(required=True, validate=(required))
    id = fields.Int(required=False)
    createdOn = fields.Str(required=False)
    createdBy = fields.Int(required=False)
    Images = fields.Str(required=False)
    status = fields.Str(required=False)
    Videos = fields.Str(required=False)


@api.route('/redflags', methods=['POST'])
@authenticate
def create_redflag(identity):
    #creating a red-flag
    data, errors = IncidentSchema().load(request.get_json())
    
    if errors:
            return jsonify({
              "errors": errors, 
              "status": 400}), 400

    return create_incident(identity, data, 'red-flag')

@api.route('/interventions', methods=['POST'])
@authenticate
def create_intervension(identity):
    #creating a red-flag
    data, errors = IncidentSchema().load(request.get_json())
    
    if errors:
            return jsonify({
              "errors": errors, 
              "status": 400}), 400

    return create_incident(identity, data, 'intervention')

def create_incident(identity, data, type):
    # creating an incident
    createdBy = identity
    incident = Incident(createdBy, type, data['location'],
                data['status'],
                data['Images'], data['Videos'], data['comment'])
    response = incident.create_incident()
    return response


@api.route('/interventions', methods=['GET'])
@authenticate
def get_interventions(identity):
    # getting all interventions
    return get_incidents('intervention', identity)


@api.route('/red-flags', methods=['GET'])
@authenticate
def get_redflags(identity):
    # getting all redflags
    return get_incidents('red-flag', identity)


def get_incidents(type, identity):
    incidents = ()

    if isAdmin(identity) == True:
        cur.execute("select * from incidents where type = '{}'".format(type))
        incidents = cur.fetchall()
    else:
        cur.execute("select * from incidents where type = '{}' and createdBy = '{}'".format(type, identity))
        incidents = cur.fetchall()
        
    if not incidents:
        return jsonify({
        "status" : 200,
        "message": "There are no " + type + "s"
        }), 200

    cur.close()
    return jsonify({
        "status" : 200,
        "data": incidents
        }), 200


@api.route('/red-flags/<int:redflag_id>/status', methods=['PATCH'])
@authenticate
def edit_redflag_status(identity, redflag_id):
    #editing status of a red-flag record

    if isAdmin(identity) == True:
        data, errors = IncidentSchema().load(request.get_json())
        
        if errors:
                return jsonify({
                "errors": errors, 
                "status": 400}), 400
        
        if data['type'] == 'intervention':
            return jsonify({
                "errors": "You are trying to edit an intervention record, use /interventions/<int:intervention_id>/status endpoint instead", 
                "status": 400}), 400

        if not data['status'].strip(' '):
            return jsonify({
                "errors": "Red-flag status cannot be null", 
                "status": 400}), 400

        return edit_incident('status', redflag_id, data['status'], 'red-flag', identity)
    else:
         return jsonify({
                "errors": "You have no permissions to edit this record. Contact the administrator", 
                "status": 400}), 400


@api.route('/interventions/<int:intervention_id>/status', methods=['PATCH'])
@authenticate
def edit_intervention_status(identity, intervention_id):
    #editing status of an intervention record
   if isAdmin(identity) == True:
        data, errors = IncidentSchema().load(request.get_json())
        if errors:
                return jsonify({
                "errors": errors, 
                "status": 400}), 400
        
        if data['type'] == 'red-flag':
            return jsonify({
                "errors": "You are trying to edit a red-flag record, use /red-flags/<int:redflag_id>/status endpoint instead", 
                "status": 400}), 400

        if not data['status'].strip(' '):
            return jsonify({
                "errors": "Red-flag status cannot be null", 
                "status": 400}), 400

        return edit_incident('status', intervention_id, data['status'], 'intervention', identity)

   else:
       return jsonify({
                "errors": "You have no permissions to edit this record. Contact the administrator", 
                "status": 400}), 400


@api.route('/red-flags/<int:redflag_id>/location', methods=['PATCH'])
@authenticate
def edit_redflag_location(identity, redflag_id):
    #editing location of a red-flag record
    data, errors = IncidentSchema().load(request.get_json())
    
    if errors:
            return jsonify({
              "errors": errors, 
              "status": 400}), 400
    
    if data['type'] == 'intervention':
        return jsonify({
              "errors": "You are trying to edit an intervention record, use /interventions/<int:intervention_id>/location endpoint instead", 
              "status": 400}), 400

    return edit_incident('location', redflag_id, data['location'], 'red-flag', identity)


@api.route('/interventions/<int:intervention_id>/location', methods=['PATCH'])
@authenticate
def edit_intervention_location(identity, intervention_id):
    #editing status of an intervention record
    data, errors = IncidentSchema().load(request.get_json())
    
    if errors:
            return jsonify({
              "errors": errors, 
              "status": 400}), 400
    
    if data['type'] == 'red-flag':
        return jsonify({
              "errors": "You are trying to edit a red-flag record, use /red-flags/<int:redflag_id>/location endpoint instead", 
              "status": 400}), 400

    return edit_incident('location', intervention_id, data['location'], 'intervention', identity)


@api.route('/interventions/<int:intervention_id>/comment', methods=['PATCH'])
@authenticate
def edit_intervention_comment(identity, intervention_id):
    #editing status of an intervention record
    data, errors = IncidentSchema().load(request.get_json())
    
    if errors:
            return jsonify({
              "errors": errors, 
              "status": 400}), 400
    
    if data['type'] == 'red-flag':
        return jsonify({
              "errors": "You are trying to edit a red-flag record, use /red-flags/<int:redflag_id>/comment endpoint instead", 
              "status": 400}), 400

    return edit_incident('comment', intervention_id, data['comment'], 'intervention', identity)


@api.route('/red-flags/<int:redflag_id>/comment', methods=['PATCH'])
@authenticate
def edit_redflag_comment(identity, redflag_id):
    #editing status of a red-flag record
    data, errors = IncidentSchema().load(request.get_json())
    
    if errors:
            return jsonify({
              "errors": errors, 
              "status": 400}), 400
    
    if data['type'] == 'intervention':
        return jsonify({
              "errors": "You are trying to edit an intervention record, use /interventions/<int:intervention_id>/comment endpoint instead", 
              "status": 400}), 400

    return edit_incident('comment', redflag_id, data['comment'], 'red-flag', identity)


def edit_incident(update_type, update_record, incident_id, type, indentity):
    #function for editing incidents
    cur.execute("select * from incidents where id = '{}'".format(incident_id))
    incident = cur.fetchone()

    if not incident:
        return jsonify({
        "status" : 200,
        "message": "The " + type + " record was not found"
        }), 200
        
    if verified(indentity) == True:
        query = "update incidents set " + update_type + " = '{}' where id = {}".format(update_record, incident_id)
        cur.execute(query)
        cur.close()
        conn.commit()
        return jsonify({
        "status" : 200,
        "message": "Updated " + incident['type'] + " record " + update_type
        }), 200
    else:
        return jsonify({
        "status" : 401,
        "message": "You have no permissions to edit this record"
        }), 401



@api.route('/redflags/<int:redflag_id>', methods=['GET'])
@authenticate
def get_single_redflag(identity, redflag_id):
    #getting a single redflag
    return get_single_incident(redflag_id)


@api.route('/interventions/<int:intervention_id>', methods=['GET'])
@authenticate
def get_single_intervention(identity, intervention_id):
    #getting a single redflag
    return get_single_incident(intervention_id)


def get_single_incident(incident_id):
    cur.execute("select * from incidents where id = '{}'".format(incident_id))
    incident = cur.fetchone()

    if not incident:
        return jsonify({
        "status" : 200,
        "message": "The " + type + " record was not found"
        }), 200

    return jsonify({
    "status" : 200,
    "data": incident
    }), 200


@api.route('/redflags/<int:redflags_id>', methods=['GET'])
@authenticate
def delete_redflag(identity, redflags_id):
    #deleting a red-flag record 
    return delete_incident(redflags_id, 'red-flag')


@api.route('/interventions/<int:intervention_id>', methods=['GET'])
@authenticate
def delete_intervention(identity, intervention_id):
    #deleting an intervention record
    return delete_incident(intervention_id, 'intervention')


def delete_incident(incident_id, type):
    cur.execute("select * from incidents where id = '{}'".format(incident_id))
    incident = cur.fetchone()

    if not incident:
        return jsonify({
        "status" : 200,
        "message": "The " + type + " record was not found"
        }), 200

    cur.execute("delete * from incidents where id = {}".format(incident_id))
    cur.close()
    conn.commit()
    return jsonify({
        "message": type + " record was deleted"
        }), 200


def isAdmin(user_id):
    cur.execute("select * from users where id = '{}'".format(user_id))
    user = cur.fetchone()
    return user[9]

def verified(user_id):
    cur.execute("select * from incidents where createdBy = '{}'".format(user_id))
    incident = cur.fetchone()
    if not incident and isAdmin(user_id) == False:
        return False
    return True





#    if isAdmin(identity) == True:
        
#    else:
#        return jsonify({
#                 "errors": "You have no permissions to edit this record. Contact the administrator", 
#                 "status": 400}), 400