from flask import Flask, jsonify, request
from marshmallow import ValidationError, Schema, fields
from psycopg2.extras import RealDictCursor
import datetime
import smtplib

from app import app
from app.api.v2.models.incident import Incident
from app.api.v2.common.validator import email, required, verifyStatus, verifyType
from app.api.v2.views import api
from app.api.v2.common.authenticator import authenticate
from app.db.config import open_connection, close_connection
from app.api.v2.views.errors import error_response

email = ""
password = ""
conn = open_connection()
cur = conn.cursor(cursor_factory=RealDictCursor)


class IncidentSchema(Schema):
    # Represents the schema for incidents
    type = fields.Str(required=False)
    comment = fields.Str(required=True, validate=(required))
    location = fields.Str(required=True, validate=(required))
    id = fields.Int(required=False)
    createdOn = fields.Str(required=False)
    createdBy = fields.Int(required=False)
    Images = fields.Str(required=False)
    status = fields.Str(required=False)
    Videos = fields.Str(required=False)


class IncidentStatusSchema(Schema):
    # Represents the schema for incidents status edit
    type = fields.Str(required=True, validate=(verifyType))
    comment = fields.Str(required=True, validate=(required))
    location = fields.Str(required=True, validate=(required))
    id = fields.Int(required=False)
    createdOn = fields.Str(required=False)
    createdBy = fields.Int(required=False)
    Images = fields.Str(required=False)
    status = fields.Str(required=True, validate=(verifyStatus))
    Videos = fields.Str(required=False)


@api.route('/redflags', methods=['POST'])
@authenticate
def create_redflag(identity):
    # creating a red-flag
    if not isAdmin(identity):
        data, errors = IncidentSchema().load(request.get_json())

        if errors:
            return jsonify({
                "errors": errors,
                "status": 400}), 400

        return create_incident(identity, data, 'red-flag')
    return error_response(403, "Administrator cannot create an incident record")


@api.route('/interventions', methods=['POST'])
@authenticate
def create_intervension(identity):
    # creating a red-flag
    if not isAdmin(identity):
        data, errors = IncidentSchema().load(request.get_json())

        if errors:
            return jsonify({
                "errors": errors,
                "status": 400}), 400

        return create_incident(identity, data, 'intervention')
    return error_response(403, "Administrator cannot create an incident record")


def create_incident(identity, data, type):
    # creating an incident
    createdBy = identity
    status = 'draft'
    incident = Incident(createdBy, type, data['location'],
                        status,
                        data['Images'], data['Videos'], data['comment'])
    response = incident.create_incident()
    return response


@api.route('/interventions', methods=['GET'])
@authenticate
def get_interventions(identity):
    # getting all interventions
    return get_incidents('intervention', identity)


@api.route('/redflags', methods=['GET'])
@authenticate
def get_redflags(identity):
    # getting all redflags
    return get_incidents('red-flag', identity)


def get_incidents(type, identity):
    incidents = ()

    if isAdmin(identity):
        cur.execute("select * from incidents where type = '{}'".format(type))
        incidents = cur.fetchall()
    else:
        cur.execute(
            "select * from incidents where type = '{}' and createdBy = '{}'".format(type, identity))
        incidents = cur.fetchall()

    if not incidents:
        return jsonify({
            "status": 404,
            "message": "There are no " + type + "s"
        }), 404

    return jsonify({
        "status": 200,
        "data": incidents
    }), 200


@api.route('/redflags/<int:redflag_id>/status', methods=['PATCH'])
@authenticate
def edit_redflag_status(identity, redflag_id):
    # editing status of a red-flag record

    if isAdmin(identity):
        data, errors = IncidentStatusSchema().load(request.get_json())

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

        return edit_incident(
            'status',
            redflag_id,
            data['status'],
            'red-flag',
            identity)
    else:
        return error_response(403, "You do not have permissions to access this record")


@api.route('/interventions/<int:intervention_id>/status', methods=['PATCH'])
@authenticate
def edit_intervention_status(identity, intervention_id):
    # editing status of an intervention record

    if isAdmin(identity):
        data, errors = IncidentStatusSchema().load(request.get_json())
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

        return edit_incident(
            'status',
            intervention_id,
            data['status'],
            'intervention',
            identity)

    else:
        return error_response(403, "You do not have permissions to access this record")


@api.route('/redflags/<int:redflag_id>/location', methods=['PATCH'])
@authenticate
def edit_redflag_location(identity, redflag_id):
    # editing location of a red-flag record
    data, errors = IncidentSchema().load(request.get_json())

    if errors:
        return jsonify({
            "errors": errors,
            "status": 400}), 400

    if not data['type'].strip(' '):
        return jsonify({
            "errors": "type cannot be null",
            "status": 400}), 400

    if data['type'] == 'intervention':
        return jsonify({
            "errors": "You are trying to edit an intervention record, use /interventions/<int:intervention_id>/location endpoint instead",
            "status": 400}), 400

    return edit_incident(
        'location',
        redflag_id,
        data['location'],
        'red-flag',
        identity)


@api.route('/interventions/<int:intervention_id>/location', methods=['PATCH'])
@authenticate
def edit_intervention_location(identity, intervention_id):
    # editing status of an intervention record
    data, errors = IncidentSchema().load(request.get_json())

    if errors:
        return jsonify({
            "errors": errors,
            "status": 400}), 400

    if not data['type'].strip(' '):
        return jsonify({
            "errors": "type cannot be null",
            "status": 400}), 400

    if data['type'] == 'red-flag':
        return jsonify({
            "errors": "You are trying to edit a red-flag record, use /red-flags/<int:redflag_id>/location endpoint instead",
            "status": 400}), 400

    return edit_incident(
        'location',
        intervention_id,
        data['location'],
        'intervention',
        identity)


@api.route('/interventions/<int:intervention_id>/comment', methods=['PATCH'])
@authenticate
def edit_intervention_comment(identity, intervention_id):
    # editing status of an intervention record
    data, errors = IncidentSchema().load(request.get_json())

    if errors:
        return jsonify({
            "errors": errors,
            "status": 400}), 400

    if data['type'] == 'red-flag':
        return jsonify({
            "errors": "You are trying to edit a red-flag record, use /red-flags/<int:redflag_id>/comment endpoint instead",
            "status": 400}), 400

    return edit_incident(
        'comment',
        intervention_id,
        data['comment'],
        'intervention',
        identity)


@api.route('/redflags/<int:redflag_id>/comment', methods=['PATCH'])
@authenticate
def edit_redflag_comment(identity, redflag_id):
    # editing status of a red-flag record
    data, errors = IncidentSchema().load(request.get_json())

    if errors:
        return jsonify({
            "errors": errors,
            "status": 400}), 400

    if data['type'] == 'intervention':
        return jsonify({
            "errors": "You are trying to edit an intervention record, use /interventions/<int:intervention_id>/comment endpoint instead",
            "status": 400}), 400

    return edit_incident(
        'comment',
        redflag_id,
        data['comment'],
        'red-flag',
        identity)


def edit_incident(update_type, incident_id, update_record, type, indentity):
    # function for editing incidents
    cur.execute(
        "select * from incidents where id = '{}' and type = '{}'".format(incident_id, type))
    incident = cur.fetchone()

    if incident is None:
        return jsonify({
            "status": 404,
            "message": "The " + type + " record was not found"
        }), 404

    if verified(indentity):
        query = "update incidents set " + update_type + \
            " = '{}' where id = '{}'".format(update_record, incident_id)
        cur.execute(query)
        if update_type == 'status':
            sendEmail(indentity, type, update_record)
        return jsonify({"status": 200, "message": "Updated " +
                        incident['type'] + " record's " + update_type}), 200
    else:
        return error_response(403, "You do not have permissions to access this record")


@api.route('/redflags/<int:redflag_id>', methods=['GET'])
@authenticate
def get_single_redflag(identity, redflag_id):
    # getting a single redflag
    if verified(identity):
        return get_single_incident(redflag_id, 'red-flag')
    else:
        return error_response(403, "You do not have permissions to access this record")


@api.route('/interventions/<int:intervention_id>', methods=['GET'])
@authenticate
def get_single_intervention(identity, intervention_id):
    # getting a intervention redflag
    if verified(identity):
        return get_single_incident(intervention_id, 'intervention')
    else:
        return error_response(403, "You do not have permissions to access this record")


def get_single_incident(incident_id, type):
    cur.execute(
        "select * from incidents where id = '{}' and type = '{}'".format(incident_id, type))
    incident = cur.fetchone()

    if incident is None:
        return jsonify({
            "status": 404,
            "message": "The " + type + " record was not found"
        }), 404

    return jsonify({
        "status": 200,
        "data": incident
    }), 200


@api.route('/redflags/<int:redflags_id>', methods=['DELETE'])
@authenticate
def delete_redflag(identity, redflags_id):
    # deleting a red-flag record
    if verified(identity):
        return delete_incident(redflags_id, 'red-flag')
    else:
        return error_response(403, "You do not have permissions to access this record")


@api.route('/interventions/<int:intervention_id>', methods=['DELETE'])
@authenticate
def delete_intervention(identity, intervention_id):
    # deleting an intervention record
    if verified(identity):
        return delete_incident(intervention_id, 'intervention')
    else:
        return error_response(403, "You do not have permissions to access this record")


def delete_incident(incident_id, type):
    cur.execute(
        "select * from incidents where id = '{}' and type = '{}'".format(incident_id, type))
    incident = cur.fetchone()

    if not incident:
        return jsonify({
            "status": 404,
            "message": "The " + type + " record was not found"
        }), 404

    cur.execute("delete from incidents where id = '{}'".format(incident_id))
    conn.commit()
    return jsonify({
        "message": type + " record was deleted"
    }), 200


def isAdmin(user_id):
    cur.execute("select * from users where id = '{}'".format(user_id))
    user = cur.fetchone()
    return user['isadmin']


def verified(user_id):
    cur.execute(
        "select * from incidents where createdBy = '{}'".format(user_id))
    incident = cur.fetchone()
    if incident is None and isAdmin(user_id) == False:
        return False
    return True


def sendEmail(user_id, incident_type, status):
    cur.execute("select * from users where id = '{}'".format(user_id))
    user = cur.fetchone()
    FROM = email
    TO = user['email']
    SUBJECT = "iReporter Status Changed"
    TEXT = "Your " + incident_type + " status has changed to " + status

    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    try:
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(email, password)
        smtpserver.sendmail(FROM, TO, message)
        smtpserver.close()
        print('email successfully sent')
    except BaseException:
        print('email failed to send')

        
@api.route('/incidents/<int:incident_id>', methods=['PATCH'])
@authenticate
def edit_any_incident(indentity, incident_id):

    # function for editing incidents
    data, errors = IncidentSchema().load(request.get_json())

    location = data['location']
    comment = data['comment']

    cur.execute(
        "select * from incidents where id = '{}'".format(incident_id))
    incident = cur.fetchone()

    if incident is None:
        return jsonify({
            "status": 404,
            "message": "The record was not found"
        }), 404

    if verified(indentity):
        query = "update incidents set location = '{}', comment = '{}' where id = '{}'".format(
            location, comment, incident_id)
        cur.execute(query)
        return jsonify(
            {"status": 200, "message": "Record successfully updated"}), 200
    else:
        return error_response(
            403, "You do not have permissions to access this record")
    
    
@api.route('/incidents', methods=['GET'])
@authenticate
def get_all(identity):
    # getting all incidents
    return get_all_incidents(identity)


def get_all_incidents(identity):
    incidents = ()

    if isAdmin(identity):
        cur.execute("select * from incidents")
        incidents = cur.fetchall()
    else:
        cur.execute(
            "select * from incidents where createdBy = '{}'".format(identity))
        incidents = cur.fetchall()

    if not incidents:
        return jsonify({
            "status": 404,
            "message": "There are no records found"
        }), 404

    return jsonify({
        "status": 200,
        "data": incidents
    }), 200
        
        
@app.errorhandler(404)
def not_found(error):
    '''404 Error function'''
    return (jsonify({'error': 'Sorry :( We could not find what you are looking for.'}), 404)


@app.errorhandler(400)
def bad_request(error):
    '''400 Error function'''
    return (jsonify({'error': 'Error in the payload. Please verify that your payload is in the correct format'}), 400)


@app.errorhandler(405)
def method_not_allowed(error):
    '''405 Error function'''
    return (jsonify({'error': 'The method provided is not allowed for the endpoint used.'}), 405)


@app.errorhandler(500)
def server_error(error):
    '''405 Error function'''
    return (jsonify({'error': 'Oops! Something happened :( Internal server error.'}), 500)
